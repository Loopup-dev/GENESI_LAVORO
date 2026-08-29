<?php
// Iscrizione autonoma alla newsletter (form standalone in fondo alle pagine).

require_once __DIR__ . '/newsletter.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method Not Allowed');
}

if (gl_is_bot()) {
    gl_respond(true);
}

if (!gl_rate_limit_ok(6, 300)) {
    gl_respond(false, '/grazie.html', 'rate_limited');
}

$email     = gl_sanitize($_POST['email'] ?? '');
$nome      = gl_sanitize($_POST['nome']  ?? '');
$privacy   = !empty($_POST['privacy']);
$interessi = [];
foreach ((array)($_POST['interessi'] ?? []) as $i) {
    $v = gl_sanitize($i);
    if ($v !== '') $interessi[] = $v;
}

$errors = [];
if (!gl_valid_email($email)) $errors[] = 'Email non valida';
if (!$privacy)               $errors[] = 'Privacy non accettata';

if ($errors) {
    gl_respond(false, '/grazie.html', 'validation:' . implode('|', $errors));
}

$ok = gl_newsletter_add($email, $nome, 'newsletter', $interessi);

if ($ok) {
    // Conferma all'iscritto.
    $html = "<div style=\"font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#4A2B25\">
        <p>Ciao " . htmlspecialchars($nome ?: '', ENT_QUOTES, 'UTF-8') . ",</p>
        <p>ti sei iscritto agli aggiornamenti di <strong>Genesi Lavoro</strong>.</p>
        <p>Ti scriveremo quando apriamo un nuovo corso, quando esce un bando che
        potrebbe riguardarti e quando pubblichiamo qualcosa di utile sul blog.
        Niente di piu': non facciamo spam e non cediamo indirizzi a nessuno.</p>
        <p style=\"font-size:13px;color:#8C8478;margin-top:26px\">Per cancellarti basta
        rispondere a questa email scrivendo <em>cancellami</em>.</p>
        <p style=\"margin-top:24px;color:#8C8478;font-size:13px\">— Genesi Lavoro<br>
        Via Sbarre Inferiori 262, Reggio Calabria · 393 572 6245</p>
    </div>";
    $text = "Ciao,\n\nti sei iscritto agli aggiornamenti di Genesi Lavoro.\n"
          . "Ti scriveremo per nuovi corsi, bandi e articoli utili.\n\n"
          . "Per cancellarti rispondi a questa email scrivendo 'cancellami'.\n\n"
          . "- Genesi Lavoro, Via Sbarre Inferiori 262, Reggio Calabria - 393 572 6245";

    // Notifica interna + copia all'iscritto.
    gl_send_mail(
        "Nuova iscrizione newsletter — " . $email,
        "<p>Nuovo iscritto: <strong>" . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . "</strong>"
            . ($nome ? " (" . htmlspecialchars($nome, ENT_QUOTES, 'UTF-8') . ")" : "")
            . "</p><p>Interessi: " . htmlspecialchars(implode(', ', $interessi) ?: '—', ENT_QUOTES, 'UTF-8') . "</p>"
            . "<p>Totale iscritti: " . gl_newsletter_count() . "</p>",
        "Nuovo iscritto newsletter: {$email}",
        $email, $nome
    );

    // Messaggio di benvenuto separato (senza reply-to interno).
    $cfg = gl_load_config();
    try {
        $m = new \PHPMailer\PHPMailer\PHPMailer(true);
        $m->isSMTP();
        $m->Host = $cfg['host']; $m->SMTPAuth = true;
        $m->Username = $cfg['username']; $m->Password = $cfg['password'];
        $m->SMTPSecure = $cfg['encryption'] === 'ssl'
            ? \PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_SMTPS
            : \PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_STARTTLS;
        $m->Port = (int)$cfg['port']; $m->CharSet = 'UTF-8';
        $m->setFrom($cfg['from_email'], $cfg['from_name']);
        $m->addAddress($email);
        $m->isHTML(true);
        $m->Subject = 'Iscrizione confermata — Genesi Lavoro';
        $m->Body = $html; $m->AltBody = $text;
        $m->send();
    } catch (\Throwable $e) {
        gl_log('newsletter welcome: ' . $e->getMessage());
    }
}

gl_respond($ok, '/grazie.html?tipo=newsletter', $ok ? null : 'save_failed');
