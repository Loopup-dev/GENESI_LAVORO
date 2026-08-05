# Locandine Corsi — Brief & Prompt per Claude Design

> Documento da consegnare a **claude.ai/design** per generare in modo standardizzato tutte le locandine dei corsi Genesi Lavoro. La palette e i font riprendono il sito. Le locandine devono essere coerenti tra loro (stesso layout, stessa gerarchia, stesso footer istituzionale).

---

## Come si usa questo documento

1. Apri [claude.ai/design](https://claude.ai/design) → **New Project** (o continua chat esistente)
2. Trascina/allega alla chat questi file di riferimento (li trovi in questo repo):
   - `assets/logo.jpg` — logo albero
   - `assets/brand/logo-hires.png` — logo hi-res 3525×3501
   - `assets/brand/wordmark-hires.jpg` — wordmark istituzionale
   - `assets/brand/sanremorock-2023-poster.jpg` — esempio poster con loghi istituzionali
3. Copia il **Prompt finale** (in fondo a questo documento) nella chat
4. Attendi che Claude Design generi le locandine (tipicamente 2-3 varianti per corso)
5. Scaricale come PNG → riportamele qui su Claude Code → le carico nel repo in `assets/corsi/`
6. Nel sito, ogni card corso userà la locandina relativa come immagine

---

## 1. Contesto brand

**Chi è Genesi Lavoro:**
Ente del Terzo Settore, scuola di formazione professionale accreditata dalla Regione Calabria (D.D. N. 3251 del 25.03.2022). Fondata a Reggio Calabria nel 2018. Missione: dare al territorio competenze qualificanti che diventano lavoro. Collabora con enti pubblici (Regione, Città Metropolitana, INPS, Centro per l'Impiego) per erogare anche corsi gratuiti (GOL, bandi regionali, SFL).

**Tone visivo:**
Caldo, mediterraneo, editoriale. Istituzionale ma **user-friendly** — l'utente medio è un cittadino calabrese in cerca di formazione, non un designer né uno startupper. Deve sentirsi accolto, non chic-freddo.

**Cosa evitare (fondamentale):**
- Estetica "fuffaguru" (motivazionale-startup, "cambia la tua vita in 30 giorni", frecce esplosive, faccine)
- Estetica corporate-fintech (blu freddo, chip, robot, ingranaggi tech)
- Foto stock generiche (persone in giacca che sorridono davanti a laptop)
- Palette fredde o fluo

---

## 2. Design system — Palette esatta

Da usare **solo questi colori** (hex esatti dal sito):

| Ruolo | Hex | Uso |
|---|---|---|
| Marrone espresso | `#4A2B25` | Testo primario, wordmark, sfondo scuro card |
| Terracotta | `#8A4B3A` | Testo secondario, decorazioni, italic |
| Oro / ottone | `#B8925A` | CTA, accento premium, cornici, dettagli |
| Oro chiaro | `#E4C689` | Highlight, glow, sfondo pillole |
| Verde salvia | `#7C8A5A` | Badge "gratuito", "GOL", crescita, natura |
| Rosa polvere | `#C98BA8` | Solo per eventi culturali (opzionale, sparingly) |
| Crema | `#F7F3EC` | Sfondo principale |
| Avorio | `#FBF8F2` | Sfondo card, contenitori |
| Seppia | `#8C8478` | Testo terziario, meta info |

**Regola:** ogni locandina usa **max 4 colori** della palette (1 sfondo + 1 testo primario + 1 accento + eventuale badge). Non mescolare tutto.

---

## 3. Design system — Typography

Font ufficiali del brand (Google Fonts, gratuiti):

- **Display / Titoli:** `Playfair Display` — pesi 500, 600, 700, anche italic
- **Body / Info:** `Inter` — pesi 400, 500, 600, 700
- **Occasionalmente italic emozionale:** `Cormorant Garamond` italic

**Regola:** massimo 2 famiglie per locandina (Playfair per titolo + Inter per resto). Nessun font handwritten, script, o display "urlato".

---

## 4. Formato locandine — Specifica

**Formato standard obbligatorio:** `1080 × 1350 px` (aspect ratio **4:5 portrait**)

**Perché 4:5:**
- Instagram feed post (formato ottimale che occupa più schermo del quadrato)
- Facebook post ok
- Web card sito (adattabile)
- Se serve stampa A4, si può poi upscalare/adattare — ma partiamo dal digitale

**Safe zone:** contenuti importanti dentro il **rettangolo centrale al 78%** (margine 12% per lato). Titoli e loghi mai al bordo.

**Contrast ratio:** testo su sfondo deve rispettare **min 4.5:1** (accessibilità AA). Con la nostra palette:
- `#4A2B25` marrone su `#F7F3EC` crema = 11.2:1 ✓
- `#4A2B25` marrone su `#B8925A` oro = 4.9:1 ✓
- `#F7F3EC` crema su `#4A2B25` marrone = 11.2:1 ✓
- Da evitare: `#B8925A` oro su `#F7F3EC` crema = 2.6:1 ✗ (usa solo per dettagli decorativi, non testo)

---

## 5. Layout standard — Elementi obbligatori

Ogni locandina deve contenere questi 8 elementi, nella gerarchia indicata:

```
┌─────────────────────────────────────┐
│  [logo albero]      [wordmark]      │  ← 1. HEADER (top 12%)
│                                     │
│  ─────                              │
│  AREA FORMATIVA                     │  ← 2. AREA (pill/eyebrow)
│                                     │
│  TITOLO DEL                         │  ← 3. TITOLO CORSO
│  CORSO                              │     (Playfair, prominente)
│                                     │
│  Descrizione breve del corso        │  ← 4. SOTTOTITOLO
│  in 1-2 righe, tono istituzionale.  │     (Inter, medium)
│                                     │
│  [GRATUITO GOL]  [Durata 400h]      │  ← 5. BADGE FINANZIAMENTO + DURATA
│                                     │
│  Sbocchi: RSA, ospedali,            │  ← 6. SBOCCHI LAVORATIVI
│  assistenza domiciliare             │
│                                     │
│  ┌────────────────────────────┐    │
│  │  PRENOTA UN COLLOQUIO  →   │    │  ← 7. CTA
│  └────────────────────────────┘    │
│                                     │
│  ─────────────────────────────────  │
│  [UE] [Regione] [Città Metropolitana]│  ← 8. FOOTER ISTITUZIONALE
│  Accreditati D.D. 3251/2022         │
│  Via Sbarre Inferiori 262 · RC      │
│  0965 375421 · genesilavoro.it      │
└─────────────────────────────────────┘
```

### Dettagli per elemento

**1. Header (top 12%)** — logo albero (48-64 px) + wordmark testuale "Genesi Lavoro" (Playfair 700, 22px)

**2. Area formativa** — pill/badge orizzontale, colore dipende dall'area:
- Socio-sanitaria → sfondo `#8A4B3A` (terracotta), testo bianco
- Meccatronica → sfondo `#4A2B25` (marrone), testo `#B8925A` oro
- Informatica → sfondo `#7C8A5A` (salvia), testo bianco
- Amministrazione → sfondo `#B8925A` (oro), testo `#4A2B25`
- Spettacolo/Audio → sfondo `#C98BA8` (rosa), testo `#4A2B25`
- Ho.Re.Ca → sfondo `#E4C689` (oro chiaro), testo `#4A2B25`

**3. Titolo corso** — Playfair Display 600-700, 48-64px, colore `#4A2B25` marrone. Max 2 righe.

**4. Sottotitolo** — Inter 400-500, 18-20px, colore `#4A2B25` con opacità 75%. Max 2 righe.

**5. Badge finanziamento + durata** — 2 pillole affiancate:
- **Se gratuito:** badge sfondo `#7C8A5A` salvia, testo bianco "GRATUITO via GOL" (o "Bando XX" — dipende dal bando specifico)
- **Se a pagamento:** badge sfondo `#B8925A` oro, testo `#4A2B25` "Rate disponibili"
- **Se finanziabile:** badge sfondo `#B8925A` oro contornato, testo `#4A2B25` "Finanziabile"
- **Durata:** pillola bordo `#4A2B25`, testo `#4A2B25` "1.000 ore" o "400 ore" ecc

**6. Sbocchi** — Inter 400, 15-16px, colore `#4A2B25` con opacità 75%. Max 2 righe. Formato: "Sbocchi: xxx, yyy, zzz."

**7. CTA** — bottone pillola full-width o larghezza fissa 400px:
- Sfondo `#4A2B25` marrone, testo `#F7F3EC` crema, "Prenota un colloquio →" oppure "Iscriviti / Candidati →"
- Height min 56px, testo Inter 600, 16px

**8. Footer istituzionale** — righa sottile separatrice + loghi UE / Regione Calabria / Città Metropolitana + testo:
- "Ente accreditato Regione Calabria — D.D. N. 3251 del 25.03.2022"
- "Via Sbarre Inferiori 262, 89129 Reggio Calabria — Tel 0965 375421"
- "formazione@genesilavoro.it — www.genesilavoro.it"

---

## 6. Motivo visivo del brand — L'albero

**Elemento grafico ricorrente:** l'albero-da-libro del logo (metafora "dalla conoscenza al lavoro"). Da inserire come:
- **Watermark decorativo** dietro/sotto il contenuto, opacità 6-10%, dimensioni grandi (ingombra 40% dell'area)
- **Piccolo simbolo** accanto al titolo o nel footer
- **Silhouette stilizzata dei rami** come divisore tra sezioni

Non serve sempre — usalo su 60% delle locandine per non appesantire.

---

## 7. Corsi da produrre (template — da confermare/completare col cliente)

> ⚠️ Dati **da confermare col cliente**: durate, prezzi, requisiti reali. Qui sono placeholder ragionevoli basati su `Genesi_Corsi_Eventi.xlsx` e sul brief `04_CONTENUTI_COPY.md`.

### Area SOCIO-SANITARIA

**1. OSS — Operatore Socio Sanitario**
- Titolo: "OSS — Operatore Socio Sanitario"
- Sottotitolo: "Qualifica riconosciuta Regione Calabria. Il mestiere più richiesto in Calabria."
- Badge finanziamento: "A pagamento — rate disponibili" oppure "Gratuito via GOL (se in possesso dei requisiti)"
- Durata: "1.000 ore (aula + stage)"
- Sbocchi: "RSA, strutture ospedaliere, assistenza domiciliare"

**2. OSSS — Operatore Socio Sanitario Specializzato**
- Titolo: "OSSS — OSS Specializzato"
- Sottotitolo: "Modulo di specializzazione per OSS già qualificati. Prestazioni infermieristiche di base."
- Badge finanziamento: "A pagamento — rate disponibili"
- Durata: "400 ore"
- Sbocchi: "RSA, ospedali, strutture riabilitative"

### Area SPETTACOLO / AUDIO

**3. Tecnico del Suono**
- Titolo: "Tecnico del Suono"
- Sottotitolo: "Docenti di livello nazionale. Strumentazione professionale, live e studio."
- Badge finanziamento: "Finanziabile (verifica requisiti)"
- Durata: "600 ore"
- Sbocchi: "Studio di registrazione, live, broadcast"

**4. Dizione, recitazione, doppiaggio**
- Titolo: "Dizione, Recitazione e Doppiaggio"
- Sottotitolo: "Percorso per attori e speaker professionali. Docenti dal settore doppiaggio."
- Badge finanziamento: "A pagamento — rate disponibili"
- Durata: "200 ore"
- Sbocchi: "Doppiaggio, teatro, speakeraggio radio/TV"

### Area HO.RE.CA

**5. Somministrazione Alimenti e Bevande (SAB)**
- Titolo: "SAB — Somministrazione Alimenti e Bevande"
- Sottotitolo: "Certificato obbligatorio per aprire o gestire pubblici esercizi."
- Badge finanziamento: "Gratuito via GOL"
- Durata: "100 ore"
- Sbocchi: "Bar, ristoranti, gestione pubblici esercizi"

### Area AMMINISTRAZIONE

**6. Tecnico Amministrativo Contabile**
- Titolo: "Tecnico Amministrativo Contabile"
- Sottotitolo: "Contabilità, paghe, adempimenti. Le competenze che ogni studio cerca."
- Badge finanziamento: "Gratuito via GOL"
- Durata: "300 ore"
- Sbocchi: "Studi commercialisti, uffici amministrativi aziendali"

### Area MECCATRONICA

**7. Meccatronico Auto**
- Titolo: "Meccatronico Auto"
- Sottotitolo: "Officina, diagnostica elettronica, manutenzione industriale."
- Badge finanziamento: "Finanziabile (verifica requisiti)"
- Durata: "800 ore"
- Sbocchi: "Officine di autoriparazione, aziende manutenzione"

### Area INFORMATICA

**8. Sviluppo Web Junior**
- Titolo: "Sviluppo Web Junior"
- Sottotitolo: "HTML, CSS, JavaScript, framework moderni. Portfolio finale."
- Badge finanziamento: "Finanziabile (verifica requisiti)"
- Durata: "600 ore"
- Sbocchi: "Web agency, aziende con divisione digitale, freelance"

**9. Cybersecurity Fondamenti**
- Titolo: "Cybersecurity Fondamenti"
- Sottotitolo: "Sicurezza informatica, penetration testing base, GDPR."
- Badge finanziamento: "Finanziabile"
- Durata: "400 ore"
- Sbocchi: "Junior security analyst, consulenza IT"

**10. Tecnico Hardware e Reti**
- Titolo: "Tecnico Hardware e Reti"
- Sottotitolo: "Manutenzione, cablaggio, configurazione rete aziendale."
- Badge finanziamento: "Finanziabile"
- Durata: "400 ore"
- Sbocchi: "Assistenza IT, aziende con infrastruttura interna"

---

## 8. Do & Don't visivi

### ✅ DO
- Palette brand esatta (solo hex sopra)
- Playfair per titoli + Inter per body
- Layout editoriale con gerarchia netta (1 titolo, non 3)
- Silhouette dell'albero come motivo ricorrente
- Loghi istituzionali sempre in footer
- Contrast ratio min 4.5:1
- Icone SVG line-art thin (max 1-2, non decorative sovrappopolate)
- Spazio bianco/crema respirabile

### ❌ DON'T
- Foto stock generiche di persone in giacca sorridenti (a meno che siano foto REALI dei corsisti Genesi)
- Icone tech generiche (chip, cloud, robot, ingranaggi complessi)
- Gradient viola/ciano/neon
- Font handwritten o script
- Emoji come icone (🎓 🌱 ecc. — usa SVG line-art)
- Colori fuori palette (blu freddo, magenta, verde acido)
- Frecce "esplosive" o effetti drop-shadow pesanti
- Testo urlato tutto maiuscolo (eccetto piccole label/eyebrow ≤ 12px)
- Più di 2 font per locandina
- Elementi al bordo (rispetta safe zone 12%)

---

## 9. PROMPT COPY-PASTE per claude.ai/design

Copia e incolla **letteralmente** questo prompt nella chat di Claude Design (dopo aver allegato i file di riferimento):

```
Genera per me una serie di 10 locandine per i corsi di Genesi Lavoro,
scuola di formazione professionale accreditata dalla Regione Calabria
(D.D. N. 3251/2022), sede a Reggio Calabria.

FORMATO OBBLIGATORIO (tutte le locandine):
- Dimensioni: 1080 × 1350 px (aspect ratio 4:5 portrait)
- Safe zone: contenuto dentro il 78% centrale
- Contrast min 4.5:1

PALETTE (usa SOLO questi hex, max 4 per locandina):
- Marrone espresso #4A2B25 (testo primario)
- Terracotta #8A4B3A (secondario)
- Oro/ottone #B8925A (CTA, accento premium)
- Oro chiaro #E4C689 (highlight)
- Verde salvia #7C8A5A (badge "gratuito"/"GOL")
- Rosa polvere #C98BA8 (solo eventi culturali)
- Crema #F7F3EC (sfondo)
- Avorio #FBF8F2 (card)
- Seppia #8C8478 (meta)

TYPOGRAPHY:
- Titoli: Playfair Display 600-700 (48-64px)
- Body: Inter 400-500 (16-20px)
- Massimo 2 famiglie per locandina

LAYOUT STANDARD (uguale per tutte le locandine):
1. Header top: logo albero + wordmark "Genesi Lavoro"
2. Pill area formativa colorata (colore per area, vedi sotto)
3. Titolo corso Playfair grande (max 2 righe)
4. Sottotitolo Inter medium (max 2 righe)
5. Badge finanziamento + durata (pillole)
6. Sbocchi lavorativi (1-2 righe)
7. CTA "Prenota un colloquio →" (marrone su crema)
8. Footer istituzionale: loghi UE + Regione + Città Metropolitana +
   "Accreditati D.D. 3251/2022" + indirizzo + tel

COLORE PILL AREA (obbligatorio):
- Socio-sanitaria → sfondo #8A4B3A, testo bianco
- Meccatronica → sfondo #4A2B25, testo #B8925A
- Informatica → sfondo #7C8A5A, testo bianco
- Amministrazione → sfondo #B8925A, testo #4A2B25
- Spettacolo/Audio → sfondo #C98BA8, testo #4A2B25
- Ho.Re.Ca → sfondo #E4C689, testo #4A2B25

MOTIVO VISIVO RICORRENTE:
Silhouette stilizzata dell'albero dal logo Genesi (metafora "dalla
conoscenza al lavoro"), come watermark decorativo opacità 6-10% oppure
piccolo simbolo accanto al titolo. Non su tutte — su 60% delle locandine.

TONE VISIVO:
Caldo, mediterraneo, editoriale. Istituzionale ma accessibile
(l'utente medio è un cittadino calabrese in cerca di formazione).
NON estetica startup/motivazionale, NON corporate fintech,
NON foto stock generiche.

CORSI DA GENERARE (10):

1. OSS — Operatore Socio Sanitario
   Area: Socio-sanitaria
   Sottotitolo: "Qualifica riconosciuta Regione Calabria. Il mestiere
   più richiesto in Calabria."
   Finanziamento: "A pagamento — rate disponibili" (badge oro)
   Durata: 1.000 ore
   Sbocchi: "RSA, strutture ospedaliere, assistenza domiciliare"

2. OSSS — Operatore Socio Sanitario Specializzato
   Area: Socio-sanitaria
   Sottotitolo: "Modulo di specializzazione per OSS già qualificati."
   Finanziamento: "A pagamento — rate disponibili"
   Durata: 400 ore
   Sbocchi: "RSA, ospedali, strutture riabilitative"

3. Tecnico del Suono
   Area: Spettacolo/Audio
   Sottotitolo: "Docenti di livello nazionale. Live e studio."
   Finanziamento: "Finanziabile (verifica requisiti)"
   Durata: 600 ore
   Sbocchi: "Studio di registrazione, live, broadcast"

4. Dizione, Recitazione e Doppiaggio
   Area: Spettacolo/Audio
   Sottotitolo: "Per attori e speaker professionali."
   Finanziamento: "A pagamento — rate disponibili"
   Durata: 200 ore
   Sbocchi: "Doppiaggio, teatro, speakeraggio radio/TV"

5. SAB — Somministrazione Alimenti e Bevande
   Area: Ho.Re.Ca
   Sottotitolo: "Certificato per aprire o gestire pubblici esercizi."
   Finanziamento: "Gratuito via GOL" (badge salvia)
   Durata: 100 ore
   Sbocchi: "Bar, ristoranti, gestione pubblici esercizi"

6. Tecnico Amministrativo Contabile
   Area: Amministrazione
   Sottotitolo: "Contabilità, paghe, adempimenti."
   Finanziamento: "Gratuito via GOL"
   Durata: 300 ore
   Sbocchi: "Studi commercialisti, uffici amministrativi aziendali"

7. Meccatronico Auto
   Area: Meccatronica
   Sottotitolo: "Officina, diagnostica elettronica, manutenzione."
   Finanziamento: "Finanziabile"
   Durata: 800 ore
   Sbocchi: "Officine di autoriparazione, aziende manutenzione"

8. Sviluppo Web Junior
   Area: Informatica
   Sottotitolo: "HTML, CSS, JavaScript, framework moderni. Portfolio."
   Finanziamento: "Finanziabile"
   Durata: 600 ore
   Sbocchi: "Web agency, aziende con divisione digitale, freelance"

9. Cybersecurity Fondamenti
   Area: Informatica
   Sottotitolo: "Sicurezza informatica, penetration testing base, GDPR."
   Finanziamento: "Finanziabile"
   Durata: 400 ore
   Sbocchi: "Junior security analyst, consulenza IT"

10. Tecnico Hardware e Reti
    Area: Informatica
    Sottotitolo: "Manutenzione, cablaggio, configurazione rete aziendale."
    Finanziamento: "Finanziabile"
    Durata: 400 ore
    Sbocchi: "Assistenza IT, aziende con infrastruttura interna"

Vorrei ricevere ogni locandina come file PNG separato,
1080×1350 px, in un pacchetto scaricabile.
Nome file suggerito: "locandina-{numero}-{slug-corso}.png"
(es. "locandina-01-oss.png", "locandina-05-sab.png").

Se qualche dato (durata, finanziamento) non ti torna, marcalo come
"[da confermare]" nel testo della locandina — così poi il cliente
conferma prima della stampa.
```

---

## 10. Cosa fare quando ricevi le locandine

1. Scaricale tutte come PNG dal tuo claude.ai/design
2. Portamele qui in questa chat di Claude Code (o zippale in un archivio) — le carico io in `assets/corsi/`
3. Modifico le card corso di `Home.dc.html` e `corsi.dc.html` perché usino le nuove locandine come immagini
4. Verifica visuale in browser
5. Commit + push

---

## 11. Note finali (revisione col cliente)

Prima della pubblicazione definitiva, la segreteria Genesi deve confermare per ogni corso:

- Titolo esatto e certificazione rilasciata
- Durata reale (ore aula + ore stage)
- Prezzo e piani di pagamento
- Requisiti di ammissione
- Prossima data di partenza
- Eventuale codice/bando specifico se gratuito

Ogni discrepanza viene corretta prima della prima esposizione (social/sito/stampa).
