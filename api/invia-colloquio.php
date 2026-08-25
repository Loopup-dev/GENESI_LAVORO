<?php
// Endpoint per il form "Prenota colloquio" (candidati.dc.html).

require_once __DIR__ . '/shared.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method Not Allowed');
}

// Honeypot: fingi successo silenzioso.
if (gl_is_bot()) {
    gl_respond(true);
}

// Rate limit.
if (!gl_rate_limit_ok(5, 300)) {
    gl_respond(false, '/grazie.html', 'rate_limited');
}

$nome     = gl_sanitize($_POST['nome']     ?? '');
$telefono = gl_sanitize($_POST['telefono'] ?? '');
$email    = gl_sanitize($_POST['email']    ?? '');
$corso    = gl_sanitize($_POST['corso']    ?? '');
$modalita = gl_sanitize($_POST['modalita'] ?? '');
$slot     = gl_sanitize($_POST['slot']     ?? '');
$data     = gl_sanitize($_POST['data']     ?? '');
$fascia   = gl_sanitize($_POST['fascia']   ?? '');
$note     = gl_sanitize($_POST['note']     ?? '');
$privacy  = !empty($_POST['privacy']);

// Validazione minima.
$errors = [];
if ($nome === '' || mb_strlen($nome) < 2) $errors[] = 'Nome mancante';
if (!gl_valid_phone($telefono))           $errors[] = 'Telefono non valido';
if ($email !== '' && !gl_valid_email($email)) $errors[] = 'Email non valida';
if (!$privacy)                            $errors[] = 'Privacy non accettata';
if ($modalita !== 'sede' && $modalita !== 'meet') $modalita = 'sede';

if ($errors) {
    gl_respond(false, '/grazie.html', 'validation:' . implode('|', $errors));
}

$mod_label = $modalita === 'meet' ? 'Google Meet' : 'In sede';
$oggetto = "Nuova richiesta di colloquio — {$nome}";

$html = "<div style=\"font-family:Arial,sans-serif;font-size:14.5px;line-height:1.55;color:#2b1a15\">
    <h2 style=\"font-family:'Playfair Display',Georgia,serif;color:#4A2B25\">Nuova richiesta di colloquio</h2>
    <table cellpadding=\"6\" cellspacing=\"0\" style=\"border-collapse:collapse\">
      <tr><td><b>Nome</b></td><td>" . htmlspecialchars($nome, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Telefono</b></td><td>" . htmlspecialchars($telefono, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Email</b></td><td>" . htmlspecialchars($email ?: '—', ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Corso di interesse</b></td><td>" . htmlspecialchars($corso ?: '—', ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Modalità</b></td><td>" . htmlspecialchars($mod_label, ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Slot Meet</b></td><td>" . htmlspecialchars($slot ?: '—', ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Data preferita</b></td><td>" . htmlspecialchars($data ?: '—', ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td><b>Fascia oraria</b></td><td>" . htmlspecialchars($fascia ?: '—', ENT_QUOTES, 'UTF-8') . "</td></tr>
      <tr><td valign=\"top\"><b>Note</b></td><td>" . nl2br(htmlspecialchars($note ?: '—', ENT_QUOTES, 'UTF-8')) . "</td></tr>
    </table>
    <p style=\"color:#8C8478;font-size:12px;margin-top:22px\">Inviato da genesilavoro.it · IP " . htmlspecialchars($_SERVER['REMOTE_ADDR'] ?? '?', ENT_QUOTES, 'UTF-8') . "</p>
</div>";

$text = "Nuova richiesta di colloquio\n"
      . "Nome: {$nome}\nTelefono: {$telefono}\nEmail: " . ($email ?: '-') . "\n"
      . "Corso: " . ($corso ?: '-') . "\nModalità: {$mod_label}\n"
      . "Slot Meet: " . ($slot ?: '-') . "\nData preferita: " . ($data ?: '-') . "\n"
      . "Fascia: " . ($fascia ?: '-') . "\nNote: " . ($note ?: '-') . "\n";

$ok = gl_send_mail(
    $oggetto,
    $html,
    $text,
    $email,           // reply-to
    $nome,
    [],
    $email ?: null    // copia di cortesia al mittente solo se ha lasciato l'email
);

gl_respond($ok, '/grazie.html?tipo=colloquio', $ok ? null : 'send_failed');
