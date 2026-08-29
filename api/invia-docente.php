<?php
// Candidatura per entrare nell'albo docenti (docenti.dc.html), con CV allegato.

require_once __DIR__ . '/newsletter.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method Not Allowed');
}

if (gl_is_bot()) {
    gl_respond(true);
}

if (!gl_rate_limit_ok(3, 300)) {
    gl_respond(false, '/grazie.html', 'rate_limited');
}

$nome       = gl_sanitize($_POST['nome']       ?? '');
$cognome    = gl_sanitize($_POST['cognome']    ?? '');
$email      = gl_sanitize($_POST['email']      ?? '');
$telefono   = gl_sanitize($_POST['telefono']   ?? '');
$titolo     = gl_sanitize($_POST['titolo']     ?? '');
$esperienza = gl_sanitize($_POST['esperienza'] ?? '');
$modalita   = gl_sanitize($_POST['modalita']   ?? '');
$messaggio  = gl_sanitize($_POST['messaggio']  ?? '');
$privacy    = !empty($_POST['privacy']);

// Ambiti selezionati (checkbox multiple)
$ambiti = [];
foreach ((array)($_POST['ambiti'] ?? []) as $a) {
    $v = gl_sanitize($a);
    if ($v !== '') $ambiti[] = $v;
}
$altro_ambito = gl_sanitize($_POST['altro_ambito'] ?? '');
if ($altro_ambito !== '') $ambiti[] = $altro_ambito;

$errors = [];
if ($nome === '')               $errors[] = 'Nome mancante';
if ($cognome === '')            $errors[] = 'Cognome mancante';
if (!gl_valid_email($email))    $errors[] = 'Email non valida';
if (!gl_valid_phone($telefono)) $errors[] = 'Telefono non valido';
if (!$ambiti)                   $errors[] = 'Nessun ambito selezionato';
if (!$privacy)                  $errors[] = 'Privacy non accettata';

// CV: obbligatorio
$cv = $_FILES['cv'] ?? null;
$dest = null;
$mime = '';
if (!$cv || ($cv['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
    $errors[] = 'CV non caricato';
} else {
    if ($cv['size'] > 8 * 1024 * 1024) $errors[] = 'CV troppo grande (max 8 MB)';
    $ext = strtolower(pathinfo($cv['name'], PATHINFO_EXTENSION));
    if (!in_array($ext, ['pdf', 'doc', 'docx'], true)) {
        $errors[] = 'Formato CV non ammesso (solo PDF/DOC/DOCX)';
    }
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mime = $finfo->file($cv['tmp_name']) ?: 'application/octet-stream';
    $ok_mime = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/octet-stream',
    ];
    if (!in_array($mime, $ok_mime, true)) $errors[] = 'MIME CV non ammesso: ' . $mime;
}

if ($errors) {
    gl_respond(false, '/grazie.html', 'validation:' . implode('|', $errors));
}

$safe = preg_replace('/[^A-Za-z0-9._-]/', '_', $nome . '_' . $cognome . '.' . $ext);
$dir  = __DIR__ . '/uploads';
if (!is_dir($dir)) @mkdir($dir, 0700, true);
$dest = $dir . '/' . uniqid('cvdoc_', true) . '_' . $safe;
if (!move_uploaded_file($cv['tmp_name'], $dest)) {
    gl_respond(false, '/grazie.html', 'upload_failed');
}

$full = trim($nome . ' ' . $cognome);
$h = fn($v) => htmlspecialchars($v ?: '—', ENT_QUOTES, 'UTF-8');

$oggetto = "Albo docenti — {$full} (" . implode(', ', array_slice($ambiti, 0, 2)) . ")";

$html = "<div style=\"font-family:Arial,sans-serif;font-size:14.5px;line-height:1.55;color:#2b1a15\">
    <h2 style=\"font-family:'Playfair Display',Georgia,serif;color:#4A2B25\">Nuova candidatura — Albo docenti</h2>
    <table cellpadding=\"6\" cellspacing=\"0\" style=\"border-collapse:collapse\">
      <tr><td><b>Nome</b></td><td>" . $h($full) . "</td></tr>
      <tr><td><b>Email</b></td><td>" . $h($email) . "</td></tr>
      <tr><td><b>Telefono</b></td><td>" . $h($telefono) . "</td></tr>
      <tr><td valign=\"top\"><b>Ambiti</b></td><td>" . $h(implode(' · ', $ambiti)) . "</td></tr>
      <tr><td><b>Titolo di studio</b></td><td>" . $h($titolo) . "</td></tr>
      <tr><td><b>Esperienza</b></td><td>" . $h($esperienza) . "</td></tr>
      <tr><td><b>Disponibilità</b></td><td>" . $h($modalita) . "</td></tr>
      <tr><td valign=\"top\"><b>Presentazione</b></td><td>" . nl2br($h($messaggio)) . "</td></tr>
      <tr><td><b>Newsletter</b></td><td>" . (!empty($_POST['newsletter']) ? 'Sì' : 'No') . "</td></tr>
    </table>
    <p><b>CV allegato:</b> " . $h(basename($cv['name'])) . " · " . round($cv['size'] / 1024) . " KB</p>
    <p style=\"color:#8C8478;font-size:12px;margin-top:22px\">Inviato da genesilavoro.it/docenti.dc.html · IP "
        . $h($_SERVER['REMOTE_ADDR'] ?? '?') . "</p>
</div>";

$text = "Nuova candidatura albo docenti\n"
      . "Nome: {$full}\nEmail: {$email}\nTelefono: {$telefono}\n"
      . "Ambiti: " . implode(', ', $ambiti) . "\n"
      . "Titolo: " . ($titolo ?: '-') . "\nEsperienza: " . ($esperienza ?: '-') . "\n"
      . "Disponibilità: " . ($modalita ?: '-') . "\n"
      . "Presentazione: " . ($messaggio ?: '-') . "\n"
      . "CV: " . basename($cv['name']) . "\n";

$ok = gl_send_mail(
    $oggetto, $html, $text, $email, $full,
    [['path' => $dest, 'name' => basename($cv['name']), 'mime' => $mime]],
    $email
);

@unlink($dest);

// Consenso newsletter, se spuntato: gli ambiti diventano interessi.
gl_newsletter_from_post($email, $full, 'docente', $ambiti);

gl_respond($ok, '/grazie.html?tipo=docente', $ok ? null : 'send_failed');
