<?php
// Endpoint per il modulo di preadesione al seminario di chitarra
// (seminario-chitarra-baglioni.html).

require_once __DIR__ . '/newsletter.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method Not Allowed');
}

if (gl_is_bot()) {
    gl_respond(true);
}

if (!gl_rate_limit_ok(5, 300)) {
    gl_respond(false, '/grazie.html', 'rate_limited');
}

$nome       = gl_sanitize($_POST['nome']       ?? '');
$telefono   = gl_sanitize($_POST['telefono']   ?? '');
$email      = gl_sanitize($_POST['email']      ?? '');
$livello    = gl_sanitize($_POST['livello']    ?? '');
$formazione = gl_sanitize($_POST['formazione'] ?? '');
$incontro   = gl_sanitize($_POST['incontro']   ?? '');
$note       = gl_sanitize($_POST['note']       ?? '');
$privacy    = !empty($_POST['privacy']);

$errors = [];
if ($nome === '' || mb_strlen($nome) < 2) $errors[] = 'Nome mancante';
if (!gl_valid_phone($telefono))           $errors[] = 'Telefono non valido';
if (!gl_valid_email($email))              $errors[] = 'Email non valida';
if ($livello === '')                      $errors[] = 'Livello mancante';
if (!$privacy)                            $errors[] = 'Privacy non accettata';

if ($errors) {
    gl_respond(false, '/grazie.html', 'validation:' . implode('|', $errors));
}

$oggetto = "Preadesione seminario chitarra (Baglioni) — {$nome}";

$h = fn($v) => htmlspecialchars($v ?: '—', ENT_QUOTES, 'UTF-8');

$html = "<div style=\"font-family:Arial,sans-serif;font-size:14.5px;line-height:1.55;color:#2b1a15\">
    <h2 style=\"font-family:'Playfair Display',Georgia,serif;color:#4A2B25\">Nuova preadesione — Seminario di chitarra acustica</h2>
    <p style=\"color:#8A4B3A;font-weight:bold;margin:0 0 18px\">Percorso con Giovanni Baglioni</p>
    <table cellpadding=\"6\" cellspacing=\"0\" style=\"border-collapse:collapse\">
      <tr><td><b>Nome</b></td><td>" . $h($nome) . "</td></tr>
      <tr><td><b>Telefono</b></td><td>" . $h($telefono) . "</td></tr>
      <tr><td><b>Email</b></td><td>" . $h($email) . "</td></tr>
      <tr><td><b>Da quanto suona</b></td><td>" . $h($livello) . "</td></tr>
      <tr><td><b>Come studia oggi</b></td><td>" . $h($formazione) . "</td></tr>
      <tr><td><b>Primo incontro 31/08</b></td><td>" . $h($incontro) . "</td></tr>
      <tr><td valign=\"top\"><b>Note</b></td><td>" . nl2br($h($note)) . "</td></tr>
    </table>
    <p style=\"color:#8C8478;font-size:12px;margin-top:22px\">Inviato da genesilavoro.it/seminario-chitarra-baglioni.html · IP "
        . htmlspecialchars($_SERVER['REMOTE_ADDR'] ?? '?', ENT_QUOTES, 'UTF-8') . "</p>
</div>";

$text = "Nuova preadesione — Seminario chitarra acustica (Giovanni Baglioni)\n"
      . "Nome: {$nome}\nTelefono: {$telefono}\nEmail: {$email}\n"
      . "Da quanto suona: " . ($livello ?: '-') . "\n"
      . "Come studia: " . ($formazione ?: '-') . "\n"
      . "Primo incontro 31/08: " . ($incontro ?: '-') . "\n"
      . "Note: " . ($note ?: '-') . "\n";

$ok = gl_send_mail($oggetto, $html, $text, $email, $nome, [], $email);

gl_newsletter_from_post($email, $nome, 'seminario', ['Musica e chitarra']);

gl_respond($ok, '/grazie.html?tipo=seminario', $ok ? null : 'send_failed');
