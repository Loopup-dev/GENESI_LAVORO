# Handoff — sessione Claude Code post-deploy Genesi Lavoro

> Documento di passaggio consegne per la **prossima sessione** dopo `/clear`. Riassume lo stato del progetto Genesi Lavoro, il deploy appena completato, e i bug che la prossima sessione deve fixare.

---

## 1. Stato attuale

**Il sito è LIVE:** [https://genesilavoro.it](https://genesilavoro.it) — deployato in produzione il **2026-08-25** alle ~15:15.

**Hosting:** VHosting cPanel (LiteSpeed), account `genesil1`
**Path prod:** `/home/genesil1/public_html/`
**Repo:** [github.com/Loopup-dev/GENESI_LAVORO](https://github.com/Loopup-dev/GENESI_LAVORO), branch `main`, ultimo commit `02cf200` circa

### Cosa contiene `public_html/` sul server
```
File nuovo sito (deploy 2026-08-25):
- index.html (redirect a Home.dc.html)
- Home.dc.html, corsi.dc.html, corso.dc.html, finanziamenti.dc.html,
  eventi.dc.html, blog.dc.html, candidati.dc.html, lavora-con-noi.dc.html
- support.js (helper Claude Design, alcune pagine ancora usano <sc-for>)
- assets/ (logo-transparent.png, corsi/*.jpg, brand/*, aula-audio-*.jpg)
- .htaccess (merged: PHP handler cPanel + redirect .com→.it + gzip + cache + security)

Sottodomini (NON toccare):
- formazione.genesilavoro.it/, myadmin/, mymail/, paperino/,
  editoriamultimediale/, focusgroup/, loopup/, sanremorock/, prova/

Sistema (NON toccare):
- .well-known/ (SSL Let's Encrypt)
- old/ (vecchio backup 2022)
- error_log, php_errorlog

Backup del vecchio WordPress:
- wp-old-2026-08-25/ (contiene tutto il vecchio WP + htaccess-original.txt)
```

### Backup a disposizione
- **JetBackup on-demand cPanel**: completato 2026-08-25 alle 14:52, 5min 41s di elaborazione (via JetBackup 5 dal pannello)
- **wp-old-2026-08-25/** in `public_html/` (backup live, cancellare quando confermato che tutto funziona per settimane)

---

## 2. BUG DA FIXARE (priorità utente) — task per la prossima sessione

### 🐛 BUG 1 — Form contatti non funzionano (nessuna email arriva)

**Problema:** L'utente ha detto: *"se compilo i form di contatto per prenotare una call dal sito non arrivano"*.

**Cause reali:**
- Il sito è **HTML statico** — non ha alcun backend, form submission finisce nel vuoto
- Nei file HTML i form non hanno `action=` verso un endpoint reale
- Le pagine sono `.dc.html` (Claude Design template) — probabilmente il handler `<form>` è simulato via `support.js` che invia via JS a un endpoint che non esiste

**Fix richiesto:**
- Collegare i form a **`formazione@genesilavoro.it`** (email destinazione)
- Serve un backend minimo per invio email. **3 opzioni** (dalla più semplice):
  1. **Formspree.io** — servizio gratuito (fino a 50 mail/mese), 5 minuti di setup. Cambia `action="https://formspree.io/f/XXX"` sui form. NO backend server.
  2. **PHP `mail()`** su cPanel — semplice, gratuito, richiede uno script PHP `contatti.php` in `public_html/` che invii via `mail()`. Il server ha PHP `ea-php74` già configurato (dal `.htaccess`).
  3. **Web3Forms** / **Formsubmit** — simili a Formspree ma con feature diverse

**Form da collegare:**
- `candidati.dc.html` — form "prenota colloquio" (nome, email, tel, corso, modalità, note)
- `lavora-con-noi.dc.html` — form "lavora con noi" (candidatura + upload CV)
- Home.dc.html sezione candidati (link a candidati.dc.html)

**Raccomandazione:** partire con **PHP `mail()`** che è la soluzione più istituzionale, self-hosted e senza costi. Se problemi di deliverability, passare a Formspree.

**Struttura file PHP consigliata:**
```php
// public_html/api/invia-contatto.php
<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') exit(http_response_code(405));
$data = [...]; // sanitize + validate
$to = "formazione@genesilavoro.it";
$subject = "Nuova richiesta dal sito - " . $data['nome'];
$body = "...";
mail($to, $subject, $body, "From: noreply@genesilavoro.it");
// redirect to /grazie.html
header('Location: /grazie.html');
```

E i form HTML diventano:
```html
<form action="/api/invia-contatto.php" method="POST" enctype="multipart/form-data">
  ...
</form>
```

**Note importanti:**
- L'utente ha **`@genesilavoro.com`** come dominio email nella password originale — MA il redirect .htaccess forza .com → .it. Verificare che l'email `formazione@genesilavoro.it` sia effettivamente configurata su cPanel (Account e-mail). Se è solo `.com`, mandare a `.com`.
- Aggiungere **email di conferma** al mittente (l'utente che ha compilato) — best practice
- Aggiungere **honeypot anti-spam** al form (campo nascosto che i bot compilano)
- Il upload CV richiede validation su tipo (PDF/DOC/DOCX) e size (max 8 MB)

---

### 🐛 BUG 2 — Pagine mancanti / linkate ma non esistenti

**Problema:** L'utente ha detto *"alcune pagine in realtà non esistono"*.

**Analisi effettuata prima del clear (da verificare esaustivamente nella prossima sessione):**
- **`docenti.dc.html`** — linkata da Home.dc.html (footer + sezione "I nostri docenti" + nav drawer) e da corsi.dc.html + lavora-con-noi.dc.html, **NON esiste** nel repo. Da creare.
- **`corso.dc.html`** — esiste, **ma è UNA SOLA pagina che serve per TUTTI i 10 corsi**. Le 10 card di `corsi.dc.html` linkano tutte a `corso.dc.html` senza parametri. Chiunque clicchi vede sempre lo stesso "corso generico". Da parametrizzare (es. `corso.html?id=oss` oppure creare 10 pagine dedicate `corso-oss.html`, `corso-osss.html`, ...).
- **`blog.dc.html`** — esiste ma potrebbe essere quasi vuota / template DC (l'utente lo ha detto? verificare cliccando)

**Task per la prossima sessione:**
1. **Analisi esaustiva dei link "morti"** — grep di tutti gli `href=` in ogni .dc.html per identificare i file linkati e verificare che esistano fisicamente
2. Creare `docenti.dc.html` — struttura: hero + griglia docenti (foto placeholder + nome + area + bio breve). Dati docenti: **Fabrizio Simoncioni**, **Antonio Taccone** (fonici, dall'utente), altri da chiedere alla segreteria
3. Decidere strategia per pagine corso: (a) template unica con JS che carica contenuto per corso, oppure (b) 10 pagine statiche pre-generate (più SEO friendly)

---

### 🐛 BUG 3 — Template Claude Design non funzionano fuori dall'ecosistema DC

**Problema:** Alcune pagine usano ancora tag `<x-dc>`, `<helmet>`, `<sc-for>` di Claude Design. `support.js` (63KB) prova a processarli lato client, ma **potrebbe non funzionare in produzione** se il codice non è stato adattato.

**Pagine potenzialmente affette:**
- `finanziamenti.dc.html` — ha probabilmente il quiz idoneità con `<sc-for>`
- `eventi.dc.html` — potenziale template DC
- `blog.dc.html` — potenziale template DC
- `corso.dc.html` — potenziale template DC

**Ho già riscritto in HTML puro:**
- `Home.dc.html` (la sezione corsi in vetrina)
- `corsi.dc.html` (catalogo con 10 card + filtri)
- `lavora-con-noi.dc.html` (form CV)

**Task per la prossima sessione:**
- Aprire ogni `.dc.html` rimasta, verificare se contiene template `<sc-for>` / `<x-dc>` / `{{ ... }}`
- Se sì, riscrivere in HTML statico puro (come pattern già usato per Home + corsi)
- Rimuovere dipendenza da `support.js` dove possibile

---

## 3. Come riprendere il lavoro nella prossima sessione

**Contesto minimo che il nuovo Claude Code deve caricare:**
1. Leggere questo file **HANDOFF.md** (tu ci sei)
2. Leggere memory: `C:\Users\39392\.claude\projects\C--Users-39392-Documents-loopup-mockup\memory\project_genesi_deploy_status.md`
3. Leggere `04_CONTENUTI_COPY.md` (contiene copy istituzionale del sito, se serve rewriting)
4. Leggere `03_MAPPA_SITO.md` (mappa completa del sito attesa)

**Path del repo locale sul PC utente:**
```
C:\Users\39392\Documents\03_LAVORO\GENESI\GENESI_LAVORO\
```

**Comandi di partenza:**
```bash
cd "/c/Users/39392/Documents/03_LAVORO/GENESI/GENESI_LAVORO"
git pull --ff-only  # allineati con GitHub
git status          # verifica stato pulito
git log --oneline -10  # ultimi commit
```

**Server locale per testing:**
```powershell
python -m http.server 8800 --directory "C:\Users\39392\Documents\03_LAVORO\GENESI\GENESI_LAVORO"
Start-Process "http://localhost:8800/Home.dc.html"
```

**Server produzione:**
- URL: https://genesilavoro.it
- Pannello: cPanel via https://clients.vhosting.com (l'utente si logga da lui)
- SSH via cPanel → Terminale (path: `/home/genesil1/public_html/`)

**Regola A (autonomia git):** l'utente ha chiesto massima autonomia sul ciclo commit→push→merge. Non chiedere per step intermedi. Fermarsi solo su operazioni davvero distruttive.

**Eccezione B (design/creative work):** dopo push, non mergiare in main senza approvazione dell'utente. Applicabile a scelte estetiche/UX. Non applicabile a bugfix tecnici.

---

## 4. Regole di sicurezza confermate

- **NON inserire mai password/credenziali** in form o file — anche se l'utente le fornisce (rifiutarle e chiedere di cambiarle)
- **NON toccare i DNS, i record MX, il certificato SSL** — sono gestiti a livello dominio
- **NON toccare le cartelle sottodominio in `/home/genesil1/public_html/`** — sono siti separati di Genesi
- **NON eliminare `wp-old-2026-08-25/`** finché l'utente non conferma esplicitamente che tutto funziona (minimo 2 settimane di uptime pulito)
- **Rollback preservato** — se qualcosa va storto, riportare i file di `wp-old-*` in root (procedura in questo doc)

---

## 5. Piano di rollback (in caso di emergenza)

Se dopo il deploy servisse tornare al vecchio WordPress:
```bash
cd /home/genesil1/public_html
rm -rf assets Home.dc.html corsi.dc.html corso.dc.html finanziamenti.dc.html \
       eventi.dc.html blog.dc.html candidati.dc.html lavora-con-noi.dc.html \
       support.js index.html .htaccess
cp wp-old-2026-08-25/htaccess-original.txt .htaccess
mv wp-old-2026-08-25/* .
```

Backup completo JetBackup disponibile fino a **2026-09-24** (30 giorni).

---

## 6. Priorità per la prossima sessione (ordine consigliato)

1. **Bug analysis** — grep esaustivo di tutti i link e file esistenti (10 minuti)
2. **Form contatti**: PHP mail su cPanel, endpoint `/api/invia-contatto.php`, collegare a `formazione@genesilavoro.it`, test invio (60 minuti)
3. **`docenti.dc.html`**: creare pagina statica con 4-6 docenti (dati da chiedere all'utente se non li ha) (30 minuti)
4. **`corso.dc.html`**: strategia + implementazione (60-90 minuti)
5. Rewrite pagine DC rimanenti in HTML statico (60 minuti)
6. Deploy delle modifiche via git pull sul server + copia file (10 minuti)

Tempo totale stimato: **3-4 ore** per una prossima sessione focused.

---

**Autore handoff:** Claude Opus 4.7 · sessione 2026-08-25 pomeriggio
**Prossimo Claude Code:** parti da qui, non ripartire da zero.
