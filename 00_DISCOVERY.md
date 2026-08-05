# GENESI LAVORO — Discovery & impostazione sito (documento di lavoro)

> Base di partenza per costruire insieme il prompt da consegnare a Claude Design. Contiene: dati reali raccolti,
> quadro dei finanziamenti, proposta di architettura UX, domande aperte. Il sito lo genererà Claude Design.

## 1. Dati reali (da genesilavoro.it — lug 2026, DA CONFERMARE)
- **Chi è:** scuola di formazione professionale, fondata nel **2018** a Reggio Calabria.
- **Mission (fortissima come leva narrativa):** *"abbattere gli stereotipi di un Sud Italia che non cresce"* →
  formazione qualificante + accompagnamento al lavoro + consulenza.
- **Aree formative:**
  - Socio-sanitaria: **OSS / OSSS**
  - Informatica: programmazione, **cybersecurity**, sviluppo web, sistemi di comunicazione
  - Artigianale/tecnica: **meccatronica**
  - Amministrazione/HR: operatore procedure amministrative
  - Spettacolo: **dizione, recitazione, doppiaggio**, tecnico audio/mixaggio
- **Corsi GOL gratuiti** già offerti (Garanzia Occupabilità Lavoratori).
- **Accreditamento:** collabora con Fondazione Lavoro e partner regionali → probabile **ente accreditato Regione
  Calabria** (numero accreditamento DA CONFERMARE).
- **Contatti:** Via Sbarre Inferiori 262, 89129 Reggio Calabria · Tel **0965 375421** (lun–sab 9–12 / 16–19) ·
  Email **formazione@genesilavoro.com** (⚠️ dominio sito è .it → confermare .com/.it) · Social: FB, IG, LinkedIn, WhatsApp.
- **Sito attuale (da sostituire):** sezioni Agenda, Sede, Segreteria, Servizi, carrello acquisti online.

## 2. Quadro finanziamenti / politiche attive (per le sezioni "corso gratis" e "NASPI/GOL")
### Programma GOL (Regione Calabria, PNRR) — corsi GRATUITI
- **Beneficiari:** disoccupati percettori **NASPI/DIS-COLL**, percettori di sostegno al reddito, NEET under 30,
  donne svantaggiate, over 55, disabili/fragili, disoccupati da 6+ mesi, working poor.
- **5 percorsi:** 1) Reinserimento occupazionale · 2) Upskilling (aggiornamento) · 3) Reskilling (riqualificazione)
  · 4) Lavoro e inclusione (fragili) · 5) Ricollocazione collettiva (crisi aziendali).
- **Accesso:** tramite **Centro per l'Impiego** (profilazione) → poi ente accreditato dal *Catalogo Offerta GOL*.
- **Condizionalità:** per percettori NASPI/DIS-COLL/RdC la partecipazione ai corsi è obbligatoria per mantenere il sostegno.
### Altri bandi Calabria Europa (calabriaeuropa.regione.calabria.it) — per la sezione Blog/News
- GOL **Avviso 5** (PNRR, tirocini/percorsi) · **Lavoro Giovani Calabria** · **Sistema Duale** ·
  **Incentivi formazione continua imprese** (5 mln €, domande da 28/01/2026) · **Certificazione competenze digitali** ·
  Autoimpiego · Dunamis (incentivi assunzioni). → Fonti da monitorare per il blog dei bandi.

## 3. La sfida UX
Cinque pubblici diversi in un solo sito, senza confondere nessuno. Si riducono a **3 intenti**:
1. **"Voglio formarmi e trovare lavoro"** (neodiplomati + chi vuole candidarsi) → Catalogo corsi + Candidatura.
2. **"Voglio farlo gratis / con i fondi"** (incentivi + NASPI/GOL) → Finanziamenti/GOL/Bandi + verifica idoneità.
3. **"Cerco eventi/masterclass"** → Agenda eventi.

## 4. Proposta di architettura (il "viaggio")
0. **Preloader** con logo.
1. **Hero immersivo + manifesto** — usa la mission ("il Sud che cresce"). Emozionale, alto valore, scroll cue.
2. **BIVIO INTELLIGENTE ("Da dove vuoi ripartire?")** — 3 grandi porte animate che instradano i 3 intenti.
   È il cuore del "viaggio": l'utente si auto-identifica e viene guidato.
3. **Corsi** — catalogo filtrabile per area (Socio-sanitario · IT · Meccatronica · Spettacolo · Amministrazione).
   Card premium → scheda corso → **"Candidati"**.
4. **Finanziamenti & Opportunità** — spiega GOL e bandi in modo semplice (chi può, come, gratis) +
   **strumento "Verifica se hai diritto a un corso gratuito"** (mini-quiz: NASPI? disoccupato? under 30?… → esito).
5. **Eventi & Masterclass** — agenda con prossimi eventi culturali.
6. **Chi siamo** — mission, dal 2018, numeri, accreditamento, sede/aule (cucina a vista del valore: aule, laboratori).
7. **Candidatura / Prenota un colloquio** — in sede o su **Google Meet** (booking con scelta data/ora).
8. **Blog / News bandi** — articoli sui bandi attivi (chi può accedere, come usufruirne).
9. **Contatti + mappa + footer.**

### 2 funzionalità "killer" (fanno percepire alto valore + utilità reale)
- **Verifica idoneità** (quiz finanziamenti) → risponde all'ansia n.1 dell'utente calabrese: "posso farlo gratis?".
- **Prenota colloquio** (sede/Meet) → trasforma la visita in lead concreto.

## 5. DECISIONI CONFERMATE (dal cliente)
- **Accreditamento Regione Calabria: D.D. N.3251 del 25.03.2022** → in evidenza in home (autorevolezza).
- **Struttura: IBRIDA** — home immersiva one-page + pagine dedicate (Corsi, Finanziamenti, Blog).
- **Corsi:** database in `Genesi_Corsi_Eventi.xlsx`. Prezzi = placeholder/simbolici da rifinire; **pagamento a rate** disponibile.
  Ogni corso ha una **sezione dedicata con recensioni + foto + copy tipo blog** (esperienza e opportunità).
- **Vetrina "Prossimi a partire":** gruppo di corsi (da definire quali) evidenziato in home.
- **Blog bandi:** gestito da noi a partire dallo screening; aggiornamenti periodici su richiesta in chat.
- **Colloquio/candidatura:** collegamento **WhatsApp** + **form per prenotare uno slot di call su Google Meet**.
- **Eventi:** dal file (Sanremo Rock, Progetto Agorà con Baglioni, spettacoli Auditorium Lucianum, seminari).

## 6. BRAND / PALETTE (dal logo reale)
Logo: **albero che cresce da un libro aperto**, motto **"Sapere · Saper fare · Saper essere"**; wordmark
"GENESI Lavoro" serif marrone; presenti loghi **UE + Regione Calabria + Città Metropolitana**.
Palette (chiaro/minimal/alto valore):
- Marrone espresso `#4A2B25` (primario, testo/wordmark)
- Terracotta `#8A4B3A` (secondario)
- Crema/avorio `#F7F3EC` (sfondo chiaro)
- Oro/ottone `#B8925A` (accento premium, CTA)
- Verde salvia `#7C8A5A` (accento "crescita/gratuito", dalle foglie)
- Rosa blossom (dai fiori) — solo tocchi rari
Motivo grafico ricorrente: **l'albero/la crescita** (radici nella conoscenza → fioritura nel lavoro) = il "viaggio".

## 7. Prossimi step
1. ⏳ Screening bandi (in corso) → genera `01_SCREENING_BANDI.md` + alimenta il Blog.
2. Estetica: definire con questi colori il design system.
3. Costruire il prompt completo per Claude Design (come per Attimo).
4. Da completare col cliente: durate/prezzi/recensioni/foto per corso, quali corsi in "Prossimi a partire".
