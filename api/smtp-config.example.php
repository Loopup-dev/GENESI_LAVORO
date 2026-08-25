<?php
// Template. Copia questo file in `smtp-config.php` sullo stesso path e
// compila con le credenziali reali dell'account mail su cPanel.
// smtp-config.php è escluso da git (vedi .gitignore).

return [
    // Host SMTP di cPanel per il dominio.
    // Su VHosting il valore tipico e' "mail.genesilavoro.it".
    // In caso di dubbio: cPanel -> Account e-mail -> ⚙️ del box -> Connetti dispositivi -> Impostazioni manuali.
    'host'       => 'mail.genesilavoro.it',

    // 465 = SMTPS (SSL implicito) — consigliato.
    // 587 = STARTTLS. Usa 587 solo se 465 non funziona.
    'port'       => 465,
    'encryption' => 'ssl', // 'ssl' per 465, 'tls' per 587

    // Account e-mail autenticato (deve esistere in cPanel -> Account e-mail).
    'username'   => 'formazione@genesilavoro.it',
    'password'   => 'CAMBIA_ME',

    // Da chi partono le mail. DEVE combaciare (dominio) con username per non finire in spam.
    'from_email' => 'formazione@genesilavoro.it',
    'from_name'  => 'Genesi Lavoro',

    // Destinatario delle notifiche di sito.
    'to_email'   => 'formazione@genesilavoro.it',
    'to_name'    => 'Genesi Lavoro — Segreteria',

    // Copia di cortesia (BCC) opzionale. Vuoto = disattivato.
    'bcc_email'  => '',

    // Se true logga in api/debug.log le eccezioni PHPMailer (senza credenziali).
    // Metti false in produzione dopo aver verificato che invia.
    'debug'      => true,
];
