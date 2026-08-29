<?php
// Archivio iscritti alla newsletter.
//
// Nota di progetto: qui NON si spediscono newsletter di massa. Su hosting
// condiviso l'invio massivo via SMTP finisce quasi sempre in spam e puo'
// far sospendere l'account. Questo modulo si limita a RACCOGLIERE e
// CONSERVARE gli iscritti; l'invio va fatto da un servizio dedicato
// (Brevo, Mailchimp, MailerLite) importando il CSV esportato da
// `esporta-newsletter.php`.

require_once __DIR__ . '/shared.php';

define('GL_NEWSLETTER_FILE', __DIR__ . '/data/newsletter.csv');

/**
 * Aggiunge un iscritto. Idempotente: se l'email c'e' gia', aggiorna
 * solo la data di ultimo consenso e le sorgenti.
 *
 * @param string $email
 * @param string $nome
 * @param string $sorgente  da quale form arriva (es. 'colloquio', 'seminario', 'docente')
 * @param array  $interessi elenco di aree/corsi d'interesse
 * @return bool
 */
function gl_newsletter_add(string $email, string $nome = '', string $sorgente = '', array $interessi = []): bool {
    if (!gl_valid_email($email)) return false;

    $dir = dirname(GL_NEWSLETTER_FILE);
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
        // Nessuno deve poter scaricare il file da browser.
        @file_put_contents($dir . '/.htaccess', "Require all denied\nDeny from all\n");
        @file_put_contents($dir . '/index.html', '');
    }

    $email = mb_strtolower(trim($email));
    $now   = date('c');
    $ip    = $_SERVER['REMOTE_ADDR'] ?? '';

    $righe = [];
    $trovato = false;

    if (is_file(GL_NEWSLETTER_FILE)) {
        $fh = fopen(GL_NEWSLETTER_FILE, 'r');
        if ($fh) {
            while (($r = fgetcsv($fh)) !== false) {
                if (!isset($r[0]) || $r[0] === '') continue;
                if (mb_strtolower($r[0]) === $email) {
                    $trovato = true;
                    $r[1] = $r[1] ?: $nome;
                    $sorgenti = array_filter(array_unique(array_merge(
                        explode('|', $r[2] ?? ''), [$sorgente]
                    )));
                    $r[2] = implode('|', $sorgenti);
                    $ints = array_filter(array_unique(array_merge(
                        explode('|', $r[3] ?? ''), $interessi
                    )));
                    $r[3] = implode('|', $ints);
                    $r[5] = $now; // ultimo consenso
                }
                $righe[] = $r;
            }
            fclose($fh);
        }
    }

    if (!$trovato) {
        $righe[] = [
            $email,
            $nome,
            $sorgente,
            implode('|', $interessi),
            $now,   // primo consenso
            $now,   // ultimo consenso
            $ip,
            'attivo',
        ];
    }

    // Riscrittura atomica con lock, per non perdere iscritti in caso di
    // due invii simultanei.
    $tmp = GL_NEWSLETTER_FILE . '.tmp';
    $fh = fopen($tmp, 'w');
    if (!$fh) return false;
    flock($fh, LOCK_EX);
    foreach ($righe as $r) fputcsv($fh, $r);
    fflush($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
    @rename($tmp, GL_NEWSLETTER_FILE);
    @chmod(GL_NEWSLETTER_FILE, 0640);

    return true;
}

/**
 * Legge dai POST il consenso newsletter e, se dato, registra l'iscritto.
 * Da chiamare in coda a ogni endpoint di form.
 */
function gl_newsletter_from_post(string $email, string $nome, string $sorgente, array $interessi = []): void {
    if (empty($_POST['newsletter'])) return;
    gl_newsletter_add($email, $nome, $sorgente, $interessi);
}

/** Numero di iscritti attivi. */
function gl_newsletter_count(): int {
    if (!is_file(GL_NEWSLETTER_FILE)) return 0;
    $n = 0;
    $fh = fopen(GL_NEWSLETTER_FILE, 'r');
    while (($r = fgetcsv($fh)) !== false) {
        if (!empty($r[0]) && ($r[7] ?? 'attivo') === 'attivo') $n++;
    }
    fclose($fh);
    return $n;
}
