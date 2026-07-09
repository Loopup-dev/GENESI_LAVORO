# 03 — MAPPA DEL SITO, SEZIONI & ANIMAZIONI (ibrido)

Sito **ibrido**: HOME immersiva one-page (il "viaggio") + pagine dedicate. Nav fissa minimale: logo a sinistra,
voci (Corsi · Finanziamenti · Eventi · Blog · Chi siamo), CTA oro **"Candidati"** a destra.

═══════════════════════════════════════
## HOME (one-page immersiva — il viaggio dell'albero)
═══════════════════════════════════════

0. **Preloader** — logo albero che "germoglia" + barra sottile oro; uscita con clip-path.

1. **Hero manifesto** — chiaro, ariose. Titolo emozionale sulla mission ("il Sud che cresce"). L'albero/ramo SVG
   inizia a disegnarsi. Eyebrow: "SCUOLA DI FORMAZIONE PROFESSIONALE · REGGIO CALABRIA · DAL 2018". CTA doppia:
   "Scopri i corsi" + "Verifica se puoi farlo gratis". Badge accreditamento discreto.

2. **Manifesto / chi siamo in breve** — 3 righe sulla missione + i valori "Sapere · Saper fare · Saper essere"
   che compaiono in reveal. La linea-ramo continua a crescere.

3. ⭐ **BIVIO — "Da dove vuoi ripartire?"** (cuore del viaggio)
   3 grandi porte/card animate, ognuna instrada un pubblico; hover → l'immagine cresce, appare la freccia oro:
   - 🎓 **"Voglio specializzarmi e trovare lavoro"** → /corsi
   - 💶 **"Voglio formarmi gratis o con i fondi"** → /finanziamenti (+ quiz)
   - 🎭 **"Cerco eventi e masterclass"** → /eventi
   Su mobile: 3 card impilate con reveal sfalsato.

4. **Corsi in vetrina — "Prossimi a partire"** — carosello/griglia di 3-5 corsi selezionati (card premium:
   immagine, area, nome, "gratuito/finanziabile" badge salvia, CTA "Scopri"). Link a /corsi.

5. **Finanziamenti in breve** — blocco salvia: "Tanti nostri corsi sono gratuiti." 3 icone (GOL · Bandi regionali ·
   SFL/INPS) + CTA **"Verifica se hai diritto → quiz"**.

6. **Numeri / fiducia** — count-up allo scroll: "dal 2018", "N corsi erogati", "N corsisti formati",
   "Accreditati Regione Calabria (D.D. 3251/2022)". Loghi UE/Regione/Città Metropolitana in monocromo.

7. **Eventi & Masterclass** — teaser dei prossimi 2-3 eventi (Progetto Agorà…). Link a /eventi.

8. **Chi siamo** (esteso) — la storia dal 2018, la missione, la sede/aule (foto), i docenti di prestigio.
   La fioritura dell'albero si completa qui (metafora: dalla conoscenza al lavoro).

9. **Candidati / Prenota colloquio** — CTA forte: **form colloquio** (in sede o **Google Meet**) + **WhatsApp**.

10. **Contatti + footer** — mappa Via Sbarre Inferiori 262 (stile caldo), orari (lun-sab 9-12/16-19), telefono,
    email formazione@genesilavoro.it, social, P.IVA 92104080806, badge accreditamento, loghi istituzionali.

═══════════════════════════════════════
## PAGINE DEDICATE
═══════════════════════════════════════

### /corsi — Catalogo
- Filtro per **area** (Socio-sanitario · Informatica · Meccatronica · Ambiente/Forestale · Amministrazione/HR ·
  Spettacolo/Audio · Ho.Re.Ca) e per **tipo** (Gratuito/GOL · Finanziato da bando · A pagamento con rate).
- Card corso premium → apre la **scheda corso**.

### /corsi/[singolo corso] — Scheda corso (template)
Ogni corso ha la SUA pagina con:
1. Hero corso (nome, area, badge finanziamento, durata, CTA "Candidati")
2. Descrizione + a chi è rivolto + sbocchi lavorativi + certificazione
3. **Sezione "L'esperienza"** — copy tipo blog (5-8 righe) che racconta il corso e l'opportunità
4. **Galleria foto** del corso/aula/laboratorio
5. **Recensioni** di ex corsisti (2-4)
6. **Come iscriversi / finanziamento** (se GOL: "come accedere via Centro per l'Impiego")
7. CTA finale "Candidati / Prenota colloquio"
> Nota: durate, prezzi (con **rate**), recensioni e foto sono attualmente PLACEHOLDER (vedi 04_CONTENUTI_COPY).

### /finanziamenti — "Studia (quasi) gratis"
- Spiega semplice: **GOL** (chi può, come, gratis), **bandi regionali**, **SFL-INPS**, **Garanzia Giovani**.
- ⭐ **QUIZ "Hai diritto a un corso gratuito?"** — 3-5 domande (Sei disoccupato? Percepisci NASPI/sostegno al
  reddito? Under 35? Iscritto al Centro per l'Impiego?) → esito personalizzato + CTA "Prenota un colloquio".
- Rimanda al /blog per i bandi attivi.

### /eventi — Agenda
- Prossimi eventi + archivio (Sanremo Rock 2022, Progetto Agorà con Baglioni, spettacoli Auditorium Lucianum…).
- Card evento con data, luogo, ospiti; eventuale "Prenota posto".

### /blog — News bandi & opportunità
- Articoli sui bandi attivi (fonte: 01_SCREENING_BANDI.md): chi può accedere, come usufruirne, scadenze.
- Categorie: GOL · Bandi Regione · Incentivi imprese · Autoimpiego. Gestito da noi, aggiornato periodicamente.

### /candidati — Colloquio
- **Form** (nome, telefono, email, corso di interesse, modalità: In sede / Google Meet, data-ora preferita, note)
  → invio via **email/WhatsApp**; per il Meet, prenotazione di uno **slot** (calendario).
- Pulsanti diretti: **WhatsApp** + **Chiama 0965 375421**.

### Componenti globali
- Barra "hai diritto a un corso gratis?" sticky/discreta. Cookie/privacy (GDPR). SEO locale per ogni corso.
