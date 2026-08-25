# Deploy su genesilavoro.it (VHosting)

> Guida step-by-step per pubblicare il nuovo sito sostituendo il vecchio WordPress. **Leggi tutto prima di iniziare** — un errore su un sito in produzione può bloccare il traffico o rompere le email.

---

## Cosa serve prima di partire

- [ ] Credenziali del pannello **VHosting** (cPanel/Plesk) — se non le hai, chiedile alla segreteria Genesi
- [ ] Credenziali FTP/SFTP (opzionali — il file manager del pannello basta)
- [ ] Sapere se il dominio `genesilavoro.it` è **già puntato** al piano hosting che stai usando (DNS "A record")
- [ ] Sapere se ci sono **email attive** `@genesilavoro.it` (non tocchiamo i DNS/MX se sì)
- [ ] Il file **`dist/`** o **`genesilavoro-deploy.zip`** che trovi in questo repo

---

## Passo 0 — Backup del sito attuale (OBBLIGATORIO)

Prima di toccare qualsiasi cosa, **fai un backup completo** del vecchio WordPress. Se qualcosa va storto, torni indietro in 10 minuti.

**Dal pannello VHosting:**
1. Cerca la sezione **"Backup"** (di solito nel menu principale o in Sicurezza)
2. Genera un **backup completo** che include:
   - Tutti i file di `public_html/` (o cartella equivalente della webroot)
   - Il **database MySQL** del WordPress
3. Scarica il file `.zip` o `.tar.gz` risultante **sul tuo PC** in una cartella con la data (es. `Backup_genesilavoro_2026-08-25/`)
4. Verifica che il backup contenga davvero i file (aprilo con un archiviatore)

**Attenzione:** su alcuni piani VHosting il backup automatico ha frequenza limitata. Fai un backup **manuale** ora.

---

## Passo 1 — Preparazione (raccomandato ma opzionale): staging su sottocartella

Se non sei sicuro di come si comporta il nuovo sito su VHosting, prova prima in una **sottocartella temporanea** (`/nuovo/`) senza toccare il sito principale.

1. Nel pannello, apri il **file manager** e vai in `public_html/`
2. Crea una cartella `nuovo/`
3. Upload del contenuto di `dist/` (o unzippa `genesilavoro-deploy.zip`) dentro `public_html/nuovo/`
4. Apri `https://genesilavoro.it/nuovo/` — dovresti vedere il nuovo sito
5. Testa tutto (Home, Corsi, Finanziamenti, Eventi, Blog, Docenti, Lavora con noi, Candidati) sul dominio vero
6. Se tutto ok → passa al Passo 2. Se non funziona → controlla i file mancanti o l'`.htaccess`

---

## Passo 2 — Sposta il vecchio WordPress in una cartella di backup

**NON cancellare** il vecchio WP subito — spostalo in una sottocartella. Se il nuovo sito ha problemi puoi tornare indietro senza scaricare di nuovo il backup.

**Dal file manager VHosting, in `public_html/`:**
1. Crea una cartella nuova chiamata **`wp-old-2026-08-25/`**
2. Sposta dentro tutti i file WordPress:
   - `wp-admin/`, `wp-content/`, `wp-includes/` (cartelle)
   - `wp-*.php` (tutti i file php di WP)
   - `.htaccess` (quello vecchio di WP)
   - `index.php` (di WP)
3. Alla fine, `public_html/` deve essere **vuota** (a parte la cartella `wp-old-*` e eventuale `nuovo/`)

**Se non sei sicuro cosa è di WordPress e cosa no:** sposta tutto tranne `nuovo/`. Poi al prossimo passo carichi il nuovo sito nella root pulita.

---

## Passo 3 — Upload del nuovo sito nella root

Ora `public_html/` è vuota (con solo `wp-old-*/` come backup).

**Metodo A — via file manager pannello VHosting (più semplice):**
1. Sul tuo PC, comprimi la cartella `dist/` in un unico zip → `genesilavoro-deploy.zip`
2. Nel file manager, vai in `public_html/` e **carica** il file zip
3. Click destro sul file zip → **"Estrai qui"** (o simile)
4. **Sposta il contenuto** dalla cartella `dist/` estratta direttamente in `public_html/` (o rinomina se serve)
5. Cancella il file zip dopo l'estrazione

**Metodo B — via FTP (se preferisci):**
1. Apri FileZilla (o altro client FTP)
2. Connettiti con le credenziali FTP di VHosting
3. Vai in `/public_html/`
4. Trascina tutto il contenuto della cartella locale `dist/` → carica in `public_html/`

**Alla fine, `public_html/` deve contenere:**
```
.htaccess
index.html
Home.dc.html
corsi.dc.html
corso.dc.html
finanziamenti.dc.html
eventi.dc.html
blog.dc.html
candidati.dc.html
lavora-con-noi.dc.html
support.js
assets/          (cartella con logo, foto corsi, brand asset)
wp-old-2026-08-25/    (backup del vecchio WP, non tocchiamo)
```

---

## Passo 4 — Test post-upload

Apri **`https://genesilavoro.it`** in una **finestra di navigazione privata** (per non usare la cache del vecchio sito).

Controlli:
- [ ] La home carica e mostra il logo Genesi + hero "Pianta il tuo futuro."
- [ ] Cliccando "Scopri i corsi" arrivi al catalogo con 10 card e foto
- [ ] I filtri catalogo funzionano (click su "Informatica" → 3 corsi)
- [ ] Le altre pagine caricano (corso singolo, finanziamenti, eventi, blog, candidati, lavora con noi)
- [ ] Su smartphone (o restringendo la finestra) compare l'hamburger
- [ ] Il certificato SSL è verde (lucchetto chiuso nel browser)
- [ ] Le email `@genesilavoro.it` continuano ad arrivare (invia una mail di test)

---

## Passo 5 — Certificato SSL / HTTPS

Se il vecchio sito aveva HTTPS, dovrebbe continuare a funzionare. Se compare "sito non sicuro":

1. Nel pannello VHosting cerca **"SSL / TLS"** o **"Let's Encrypt"**
2. Genera/rinnova il certificato SSL per `genesilavoro.it` e `www.genesilavoro.it`
3. Aspetta 5-10 minuti che si propaghi
4. Ricarica la pagina — il lucchetto deve essere verde
5. **Solo a questo punto** puoi attivare la riga HSTS nel `.htaccess` (è commentata; scommenta la riga con `Strict-Transport-Security`)

---

## Passo 6 — SEO (opzionale ma importante se il vecchio sito aveva visite)

Se il vecchio WordPress aveva URL tipo `/chi-siamo/`, `/corsi-oss/`, `/contatti/` che ricevono traffico da Google, chi arriva su quei URL ora vede 404 → perdi ranking.

**Cosa fare:**
1. Vai su **Google Search Console** dell'account Genesi (chiedilo a chi gestiva il sito)
2. Guarda la sezione **"Rendimento" → "Pagine"** — vedi quali URL ricevevano più clic
3. Per ognuno, aggiungi una riga nel `.htaccess` che ho preparato (sezione **"Redirect dal vecchio sito WordPress"**):
   ```apache
   RewriteRule ^chi-siamo/?$   /Home.dc.html#chisiamo   [R=301,L]
   RewriteRule ^corsi-oss/?$   /corso.dc.html            [R=301,L]
   RewriteRule ^contatti/?$    /candidati.dc.html        [R=301,L]
   ```
4. Ricarica `.htaccess` via file manager (o riupload)
5. In Search Console, sottometti una nuova **sitemap** (se ce l'hai)

Se il vecchio sito **non aveva traffico da Google**, puoi saltare questo passo.

---

## Piano di rollback (se qualcosa va storto)

Se dopo l'upload il sito non funziona o hai bisogno di tornare indietro:

1. Nel file manager, **cancella tutti i file** che hai appena caricato in `public_html/` (tranne `wp-old-*/`)
2. Sposta il contenuto di `wp-old-2026-08-25/` di nuovo nella root `public_html/`
3. Il vecchio sito WordPress torna online come prima
4. Tempo totale: 5-10 minuti

Se anche il rollback non funziona, ripristina dal **backup .zip** che hai scaricato al Passo 0.

---

## Cosa NON è cambiato (rassicurazione)

- **DNS** — non tocchiamo (il dominio resta puntato allo stesso hosting)
- **Email** `@genesilavoro.it` — continuano a funzionare (i record MX non cambiano)
- **Certificato SSL** — riutilizza quello esistente

---

## Cosa serve da me (Claude) per continuare

Perché io possa esserti più utile in questo deploy, dimmi:

1. **Che sito c'è ora su genesilavoro.it?** — È il WordPress di Genesi o un sito di un altro cliente? Se non è di Genesi, non lo possiamo sostituire.
2. **Che pannello ha VHosting?** cPanel, Plesk o altro?
3. **Ci sono email attive** `@genesilavoro.it` che ricevi/mandi ora?
4. **Il vecchio WP ha contenuti da recuperare?** (blog, iscrizioni raccolte, foto specifiche)
5. **Il vecchio sito riceve traffico da Google?** (per capire se serve fare redirect SEO)

Se rispondi a queste 5 domande ti aggiorno la checklist con istruzioni ancora più specifiche.

---

## Note finali (da consulente)

- **Non fare il cutover il venerdì pomeriggio** — se qualcosa va storto rischi di stare offline tutto il weekend con la segreteria chiusa. Fallo un martedì-mercoledì mattina, quando puoi risolvere problemi entro sera.
- **Avverti la segreteria Genesi** che stai facendo il cutover — se qualcuno chiama e dice "il sito non va", loro sanno che è normale per 10 minuti
- **Prima del cutover, testa il nuovo sito in staging** (sottocartella `/nuovo/`) — così hai già confermato che funziona
- **Il backup non è opzionale.** Fallo anche se pensi che tutto vada bene. Ti salva la vita se sbagli.
