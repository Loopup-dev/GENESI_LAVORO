<?php
// Endpoint per il form "Lavora con noi" (lavora-con-noi.dc.html) con upload CV.

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
$ruolo      = gl_sanitize($_POST['ruolo']      ?? '');
$area       = gl_sanitize($_POST['area']       ?? '');
$messaggio  = gl_sanitize($_POST['messaggio']  ?? '');
$privacy    = !empty($_POST['privacy']);

$errors = [];
if ($nome === '')            $errors[] = 'Nome mancante';
if ($cognome === '')         $errors[] = 'Cognome mancante';
if (!gl_valid_email($email)) $errors[] = 'Email non valida';
if (!gl_valid_phone($telefono)) $errors[] = 'Telefono non valido';
if ($ruolo === '')           $errors[] = 'Ruolo mancante';
if (!$privacy)               $errors[] = 'Privacy non accettata';

// Validazione CV.
$cv = $_FILES['cv'] ?? null;
if (!$cv || ($cv['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
    $errors[] = 'CV non caricato';
} else {
    $max = 8 * 1024 * 1024;
    if ($cv['size'] > $max) {
        $errors[] = 'CV troppo grande (max 8 MB)';
    }

    $allowed_ext = ['pdf', 'doc', 'docx'];
    $ext = strtolower(pathinfo($cv['name'], PATHINFO_EXTENSION));
    if (!in_array($ext, $allowed_ext, true)) {
        $errors[] = 'Formato CV non ammesso (solo PDF/DOC/DOCX)';
    }

    $allowed_mime = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/octet-stream', // alcuni browser Windows inviano questo per .doc/.docx
    ];
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mime = $finfo->file($cv['tmp_name']) ?: 'application/octet-stream';
    if (!in_array($mime, $allowed_mime, true)) {
        $errors[] = 'MIME CV non ammesso: ' . $mime;
    }
}

if ($errors) {
    gl_respond(false, '/grazie.html', 'validation:' . implode('|', $errors));
}

// Sposta il file dal tmp a una cartella dedicata prima dell'invio.
// PHPMailer legge dal path — se lasciamo il tmp, PHP potrebbe averlo gia' rimosso al momento del send.
$safe_name = preg_replace('/[^A-Za-z0-9._-]/', '_', $nome . '_' . $cognome . '.' . $ext);
$dest_dir  = __DIR__ . '/uploads';
if (!is_dir($dest_dir)) @mkdir($dest_dir, 0700, true);
$dest = $dest_dir . '/' . uniqid('cv_', true) . '_' . $safe_name;
if (!move_uploaded_file($cv['tmp_name'], $dest)) {
    gl_respond(false, '/grazie.html', 'upload_failed');
}

$full_name = trim($nome . ' ' . $cognome);
$oggetto = "Candidatura lavoro — {$full_name} ({$ruolo})";

$html = "<div style=\"font-family:Arial,sans-serif;font-size:14.5px;line-height:1.55;color:#2b1a15\">
    <h2 style=\"font-family:'Playfair Display',Georgia,serif;color:#4A2B25\">Nuova candidatura</h2>
    <table cellpadding=\"6\" cellspacing=\"0\" style=\"border-collapse:collapse\">
      <tr><td><b>Nome</b></td><td>" . htmlspecialchars($full_name, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Email</b></td><td>" . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Telefono</b></td><td>" . htmlspecialchars($telefono, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Ruolo</b></td><td>" . htmlspecialchars($ruolo, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Area</b></td><td>" . htmlspecialchars($area ?: '—', ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td valign=\"top\"><b>Presentazione</b></td><td>" . nl2br(htmlspecialchars($messaggio ?: '—', ENT_QUOTES, 'UTF-8')) . "</td></tr>
    </table>
    <p><b>CV allegato:</b> " . htmlspecialchars(basename($cv['name']), ENT_QUOTES, 'UTF-8')
        . " · " . round($cv['size'] / 1024) . " KB</p>
    <p style=\"color:#8C8478;font-size:12px;margin-top:22px\">Inviato da genesilavoro.it · IP " . htmlspecialchars($_SERVER['REMOTE_ADDR'] ?? '?', ENT_QUOTES, 'UTF-8') . "</p>
</div>";

$text = "Nuova candidatura\n"
      . "Nome: {$full_name}\nEmail: {$email}\nTelefono: {$telefono}\n"
      . "Ruolo: {$ruolo}\nArea: " . ($area ?: '-') . "\n"
      . "Presentazione: " . ($messaggio ?: '-') . "\n"
      . "CV allegato: " . basename($cv['name']) . "\n";

$ok = gl_send_mail(
    $oggetto,
    $html,
    $text,
    $email,
    $full_name,
    [['path' => $dest, 'name' => basename($cv['name']), 'mime' => $mime]],
    $email  // copia di cortesia al mittente
);

// Cleanup upload dopo invio (o dopo fallimento).
@unlink($dest);

gl_newsletter_from_post($email, $full_name, 'candidatura', array_filter([$area]));

gl_respond($ok, '/grazie.html?tipo=candidatura', $ok ? null : 'send_failed');
