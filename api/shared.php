<?php
// Helper condivisi dagli endpoint /api/. Nessuna dipendenza esterna oltre PHPMailer bundled.

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require_once __DIR__ . '/vendor/PHPMailer/Exception.php';
require_once __DIR__ . '/vendor/PHPMailer/PHPMailer.php';
require_once __DIR__ . '/vendor/PHPMailer/SMTP.php';

/**
 * Legge la config SMTP. Muore con 500 se il file manca (deploy incompleto).
 */
function gl_load_config(): array {
    $path = __DIR__ . '/smtp-config.php';
    if (!is_file($path)) {
        http_response_code(500);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => false, 'error' => 'server_misconfigured']);
        exit;
    }
    return require $path;
}

function gl_sanitize($v): string {
    if (!is_scalar($v)) return '';
    $v = (string)$v;
    $v = str_replace(["\r", "\n"], ' ', $v); // header injection guard
    return trim(strip_tags($v));
}

function gl_valid_email(string $v): bool {
    return $v !== '' && filter_var($v, FILTER_VALIDATE_EMAIL) !== false;
}

function gl_valid_phone(string $v): bool {
    $digits = preg_replace('/[^0-9]/', '', $v);
    return strlen($digits) >= 7 && strlen($digits) <= 15;
}

/**
 * Honeypot: campo hidden `website` nel form. I bot lo compilano, gli umani no.
 * Ritorna true se sospetto -> l'endpoint deve fingere successo e non inviare nulla.
 */
function gl_is_bot(): bool {
    $hp = $_POST['website'] ?? '';
    return $hp !== '';
}

/**
 * Rate limit banale file-based: massimo N richieste in W secondi per IP.
 * Ritorna true se OK, false se limite superato.
 */
function gl_rate_limit_ok(int $max = 5, int $window_seconds = 300): bool {
    $ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    $key = preg_replace('/[^a-zA-Z0-9.:_-]/', '_', $ip);
    $dir = sys_get_temp_dir() . '/gl_rl';
    if (!is_dir($dir)) @mkdir($dir, 0700, true);
    $file = $dir . '/' . $key . '.log';

    $now = time();
    $timestamps = [];
    if (is_file($file)) {
        $raw = @file_get_contents($file);
        $timestamps = array_filter(
            array_map('intval', explode("\n", trim($raw ?? ''))),
            fn($t) => $t > $now - $window_seconds
        );
    }
    if (count($timestamps) >= $max) return false;
    $timestamps[] = $now;
    @file_put_contents($file, implode("\n", $timestamps));
    return true;
}

/**
 * Log errori PHPMailer senza credenziali. Attivo solo se config['debug'] === true.
 */
function gl_log(string $msg): void {
    $cfg = gl_load_config();
    if (empty($cfg['debug'])) return;
    $line = '[' . date('c') . '] ' . $msg . "\n";
    @file_put_contents(__DIR__ . '/debug.log', $line, FILE_APPEND);
}

/**
 * Invia una mail via PHPMailer + SMTP autenticato.
 *
 * @param string   $subject      oggetto
 * @param string   $body_html    corpo HTML
 * @param string   $body_text    corpo testo (fallback)
 * @param string   $reply_to     email compilata dall'utente (opzionale)
 * @param string   $reply_name   nome compilato dall'utente (opzionale)
 * @param array    $attachments  ognuno: ['path' => string, 'name' => string, 'mime' => string]
 * @param string|null $cc_user_email  se non null, invia una copia identica al mittente
 * @return bool                  true se inviata, false su errore (loggato)
 */
function gl_send_mail(
    string $subject,
    string $body_html,
    string $body_text,
    string $reply_to = '',
    string $reply_name = '',
    array $attachments = [],
    ?string $cc_user_email = null
): bool {
    $cfg = gl_load_config();
    $mail = new PHPMailer(true);

    try {
        $mail->isSMTP();
        $mail->Host       = $cfg['host'];
        $mail->SMTPAuth   = true;
        $mail->Username   = $cfg['username'];
        $mail->Password   = $cfg['password'];
        $mail->SMTPSecure = $cfg['encryption'] === 'ssl'
            ? PHPMailer::ENCRYPTION_SMTPS
            : PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port       = (int)$cfg['port'];
        $mail->CharSet    = 'UTF-8';
        $mail->Timeout    = 20;

        $mail->setFrom($cfg['from_email'], $cfg['from_name']);
        $mail->addAddress($cfg['to_email'], $cfg['to_name']);
        if (!empty($cfg['bcc_email'])) {
            $mail->addBCC($cfg['bcc_email']);
        }
        if ($reply_to !== '' && gl_valid_email($reply_to)) {
            $mail->addReplyTo($reply_to, $reply_name ?: $reply_to);
        }

        foreach ($attachments as $a) {
            if (!empty($a['path']) && is_file($a['path'])) {
                $mail->addAttachment($a['path'], $a['name'] ?? '', 'base64', $a['mime'] ?? '');
            }
        }

        $mail->isHTML(true);
        $mail->Subject = $subject;
        $mail->Body    = $body_html;
        $mail->AltBody = $body_text;

        $mail->send();

        // Copia di cortesia al mittente (opzionale, con corpo diverso).
        if ($cc_user_email && gl_valid_email($cc_user_email)) {
            $mail2 = new PHPMailer(true);
            $mail2->isSMTP();
            $mail2->Host       = $cfg['host'];
            $mail2->SMTPAuth   = true;
            $mail2->Username   = $cfg['username'];
            $mail2->Password   = $cfg['password'];
            $mail2->SMTPSecure = $mail->SMTPSecure;
            $mail2->Port       = (int)$cfg['port'];
            $mail2->CharSet    = 'UTF-8';
            $mail2->setFrom($cfg['from_email'], $cfg['from_name']);
            $mail2->addAddress($cc_user_email);
            $mail2->isHTML(true);
            $mail2->Subject = 'Abbiamo ricevuto la tua richiesta — Genesi Lavoro';
            $mail2->Body    = gl_courtesy_html($reply_name, $subject);
            $mail2->AltBody = gl_courtesy_text($reply_name);
            $mail2->send();
        }

        return true;
    } catch (Exception $e) {
        gl_log('PHPMailer error: ' . $e->getMessage());
        return false;
    }
}

function gl_courtesy_html(string $name, string $ref_subject): string {
    $safe_name = htmlspecialchars($name ?: 'ciao', ENT_QUOTES, 'UTF-8');
    return "<div style=\"font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#4A2B25\">
        <p>Ciao {$safe_name},</p>
        <p>abbiamo ricevuto la tua richiesta e ti ricontatteremo il prima possibile.</p>
        <p>Nel frattempo, se hai bisogno di risposte rapide puoi scriverci su
        <a href=\"https://wa.me/390965375421\">WhatsApp</a> oppure chiamare
        <a href=\"tel:0965375421\">0965 375421</a> (lun–sab · 9–12 / 16–19).</p>
        <p style=\"margin-top:28px;color:#8C8478;font-size:13px\">— Segreteria Genesi Lavoro<br>
        Via Sbarre Inferiori 262, Reggio Calabria</p>
    </div>";
}

function gl_courtesy_text(string $name): string {
    $n = $name ?: 'ciao';
    return "Ciao {$n},\n\nabbiamo ricevuto la tua richiesta e ti ricontatteremo il prima possibile.\n\n"
         . "Per risposte rapide: WhatsApp https://wa.me/390965375421 · tel. 0965 375421.\n\n"
         . "— Segreteria Genesi Lavoro\nVia Sbarre Inferiori 262, Reggio Calabria";
}

/**
 * Risposta JSON o redirect. I form senza JS ricevono redirect; le fetch() ricevono JSON.
 */
function gl_respond(bool $ok, string $redirect_url = '/grazie.html', ?string $error = null): void {
    $wants_json = false;
    $accept = $_SERVER['HTTP_ACCEPT'] ?? '';
    $xrw = $_SERVER['HTTP_X_REQUESTED_WITH'] ?? '';
    if (stripos($accept, 'application/json') !== false || $xrw === 'fetch') {
        $wants_json = true;
    }

    if ($wants_json) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $error ?: 'send_failed']);
        exit;
    }

    if ($ok) {
        header('Location: ' . $redirect_url);
    } else {
        header('Location: /grazie.html?err=' . urlencode($error ?: 'send_failed'));
    }
    exit;
}
