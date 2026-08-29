#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera le pagine di dettaglio corso da `corsi-data.json`.

Perche' pagine statiche e non una sola pagina con ?id=:
- ogni corso ha un URL proprio, indicizzabile da Google ("corso OSS Reggio Calabria")
- title e meta description distinti per corso
- nessuna dipendenza da JavaScript per vedere il contenuto

Uso:
    python build_corsi.py

Rigenera `corso-<slug>.html` per ogni corso e riscrive la griglia di `corsi.dc.html`
con i link corretti.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "corsi-data.json"

BADGE_CLASS = {
    "gratuito": "card__badge--free",
    "pagamento": "card__badge--paid",
}


def badge_class_for(corso):
    """Il colore del badge segue il formato, poi il testo, poi il tipo."""
    formato = corso.get("formato", "corso")
    if formato == "seminario":
        return "card__badge--sem"
    if formato == "certificazione":
        return "card__badge--cert"
    if corso["badge"].startswith("In apertura"):
        return "card__badge--soon"
    if corso["badge"].startswith("Finanziabile"):
        return "card__badge--fin"
    return BADGE_CLASS.get(corso["tipo"], "card__badge--paid")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def li_list(items, cls=""):
    attr = f' class="{cls}"' if cls else ""
    return "\n".join(f"        <li{attr}>{esc(i)}</li>" for i in items)


PAGE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo} — Genesi Lavoro | Reggio Calabria</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://genesilavoro.it/corso-{slug}.html">
<meta property="og:title" content="{titolo} — Genesi Lavoro">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,500;0,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  *{{box-sizing:border-box}}html,body{{margin:0;padding:0}}
  body{{background:#F7F3EC;color:#4A2B25;font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.55}}
  a{{color:#8A4B3A;text-decoration:none}}a:hover{{color:#B8925A}}
  img{{max-width:100%;display:block}}
  ::selection{{background:#B8925A;color:#FBF8F2}}
  :focus-visible{{outline:2px solid #B8925A;outline-offset:3px;border-radius:6px}}

  /* NAV */
  .nav{{position:sticky;top:0;z-index:900;display:flex;align-items:center;justify-content:space-between;padding:14px 40px;background:rgba(247,243,236,.92);backdrop-filter:blur(14px);border-bottom:1px solid rgba(74,43,37,.08)}}
  .nav__brand{{display:flex;align-items:center;gap:12px;color:#4A2B25}}
  .nav__brand-badge{{width:44px;height:44px;border-radius:50%;background:#FBF8F2;box-shadow:0 3px 10px rgba(74,43,37,.1);display:flex;align-items:center;justify-content:center;flex:none}}
  .nav__brand-badge img{{width:36px;height:36px;object-fit:contain;border-radius:50%}}
  .nav__brand-name{{font-family:'Playfair Display',serif;font-weight:700;font-size:19px;display:block;line-height:1}}
  .nav__brand-sub{{font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#8C8478;margin-top:3px;display:block}}
  .nav__links{{display:flex;align-items:center;gap:26px;font-size:14px;font-weight:500}}
  .nav__links a{{color:#4A2B25}}
  .nav__cta{{font-size:13px;font-weight:600;color:#FBF8F2;background:#B8925A;padding:11px 22px;border-radius:100px;box-shadow:0 5px 16px rgba(184,146,90,.32);transition:transform .3s}}
  .nav__cta:hover{{transform:translateY(-2px);color:#FBF8F2}}
  @media(max-width:900px){{.nav__links{{display:none}}.nav{{padding:12px 20px}}}}

  /* HERO */
  .hero{{max-width:1300px;margin:0 auto;padding:52px 40px 0}}
  .hero__back{{font-size:13px;color:#8C8478;display:inline-flex;gap:6px;align-items:center}}
  .hero__grid{{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center;margin-top:26px}}
  .hero__badge{{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;padding:7px 15px;border-radius:100px;margin-bottom:20px}}
  .card__badge--free{{background:#7C8A5A;color:#FBF8F2}}
  .card__badge--fin{{background:#B8925A;color:#4A2B25}}
  .card__badge--paid{{background:#8A4B3A;color:#FBF8F2}}
  .card__badge--sem{{background:#4A2B25;color:#F7F3EC}}
  .card__badge--cert{{background:#5f6d42;color:#FBF8F2}}
  .card__badge--soon{{background:#4A2B25;color:#F0DFC0}}
  .hero__eyebrow{{font-size:12px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#B8925A;margin-bottom:14px}}
  .hero__title{{font-family:'Playfair Display',serif;font-weight:700;font-size:clamp(38px,5.6vw,74px);line-height:1;letter-spacing:-.02em;margin:0;max-width:15ch}}
  .hero__lead{{font-size:17px;line-height:1.65;color:#5c4038;margin:22px 0 28px;max-width:52ch}}
  .hero__facts{{display:flex;flex-wrap:wrap;gap:26px;padding-top:22px;border-top:1px solid rgba(74,43,37,.12)}}
  .fact__k{{font-size:10.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#8C8478;margin-bottom:5px}}
  .fact__v{{font-size:16px;font-weight:600;color:#4A2B25}}
  .hero__media img{{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:18px;box-shadow:0 24px 60px -18px rgba(74,43,37,.32)}}
  @media(max-width:900px){{.hero{{padding:34px 20px 0}}.hero__grid{{grid-template-columns:1fr;gap:32px}}}}

  /* SECTIONS */
  .wrap{{max-width:1300px;margin:0 auto;padding:0 40px}}
  @media(max-width:900px){{.wrap{{padding:0 20px}}}}
  .section{{padding:76px 0;border-top:1px solid rgba(74,43,37,.1);margin-top:76px}}
  .section:first-of-type{{border-top:0}}
  .h2{{font-family:'Playfair Display',serif;font-weight:600;font-size:clamp(28px,3.4vw,38px);line-height:1.12;margin:0 0 22px;color:#4A2B25}}
  .two-col{{display:grid;grid-template-columns:1fr 1fr;gap:56px}}
  @media(max-width:860px){{.two-col{{grid-template-columns:1fr;gap:36px}}}}
  .checklist{{list-style:none;padding:0;margin:0;display:grid;gap:13px}}
  .checklist li{{position:relative;padding-left:30px;font-size:15.5px;line-height:1.55;color:#5c4038}}
  .checklist li::before{{content:"";position:absolute;left:0;top:9px;width:14px;height:14px;border-radius:50%;background:rgba(124,138,90,.22);border:1.5px solid #7C8A5A}}
  .pill-list{{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:9px}}
  .pill-list li{{font-size:14px;font-weight:500;color:#4A2B25;background:#FBF8F2;border:1px solid rgba(74,43,37,.13);border-radius:100px;padding:9px 17px}}
  .prose{{font-size:16px;line-height:1.72;color:#5c4038;max-width:60ch;margin:0}}
  .prose em{{font-style:italic;color:#7C8A5A;font-weight:500}}

  .quote{{background:#FBF8F2;border:1px solid rgba(74,43,37,.1);border-left:3px solid #B8925A;border-radius:0 16px 16px 0;padding:30px 34px;margin-top:26px}}
  .nota{{background:rgba(184,146,90,.12);border:1px solid rgba(184,146,90,.4);border-radius:14px;padding:22px 24px;margin:26px 0 0;display:flex;gap:14px;align-items:flex-start}}
  .nota svg{{width:22px;height:22px;color:#8A4B3A;flex:none;margin-top:1px}}
  .nota p{{margin:0;font-size:14.5px;line-height:1.62;color:#5c4038}}
  .quote p{{margin:0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:21px;line-height:1.5;color:#4A2B25}}

  /* GALLERY */
  .gallery{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:8px}}
  .gallery img{{width:100%;aspect-ratio:1;object-fit:cover;border-radius:12px}}
  @media(max-width:860px){{.gallery{{grid-template-columns:repeat(2,1fr)}}}}

  /* STEPS */
  .steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:8px}}
  .step{{background:#FBF8F2;border:1px solid rgba(74,43,37,.1);border-radius:16px;padding:26px 24px}}
  .step__n{{font-family:'Playfair Display',serif;font-size:30px;color:#B8925A;line-height:1;margin-bottom:12px}}
  .step__t{{font-weight:600;font-size:16px;margin:0 0 7px}}
  .step__d{{font-size:14.5px;line-height:1.6;color:#8C8478;margin:0}}
  @media(max-width:860px){{.steps{{grid-template-columns:1fr}}}}

  /* CTA */
  .cta{{background:#4A2B25;color:#F7F3EC;margin-top:86px;padding:82px 40px;text-align:center}}
  .cta__title{{font-family:'Playfair Display',serif;font-weight:600;font-size:clamp(30px,4.4vw,52px);line-height:1.06;margin:0 auto 16px;max-width:18ch}}
  .cta__sub{{font-size:16px;line-height:1.65;color:rgba(247,243,236,.76);max-width:50ch;margin:0 auto 32px}}
  .cta__row{{display:flex;flex-wrap:wrap;gap:13px;justify-content:center}}
  .btn{{display:inline-flex;align-items:center;gap:9px;font-size:15px;font-weight:600;padding:15px 30px;border-radius:100px;transition:transform .25s}}
  .btn:hover{{transform:translateY(-2px)}}
  .btn--gold{{background:#B8925A;color:#4A2B25}}.btn--gold:hover{{color:#4A2B25}}
  .btn--ghost{{border:1.5px solid rgba(247,243,236,.3);color:#F7F3EC}}.btn--ghost:hover{{color:#F7F3EC;border-color:#B8925A}}

  /* FOOTER */
  .footer{{background:#3d231e;color:#F7F3EC;padding:40px;text-align:center}}
  .footer__motto{{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:19px;color:#B8925A;margin:0 0 7px}}
  .footer__meta{{font-size:12.5px;color:rgba(247,243,236,.65)}}
  .footer__nav{{margin-bottom:20px;display:flex;flex-wrap:wrap;gap:20px;justify-content:center;font-size:13.5px}}
  .footer__nav a{{color:rgba(247,243,236,.8)}}.footer__nav a:hover{{color:#B8925A}}
</style>
<script src="assets/analytics.js" defer></script>
</head>
<body>

<nav class="nav">
  <a href="Home.dc.html" class="nav__brand">
    <span class="nav__brand-badge"><img src="assets/logo.jpg" alt=""></span>
    <span>
      <span class="nav__brand-name">Genesi Lavoro</span>
      <span class="nav__brand-sub">Formazione Professionale</span>
    </span>
  </a>
  <div class="nav__links">
    <a href="corsi.dc.html" aria-current="page">Corsi</a>
    <a href="finanziamenti.dc.html">Finanziamenti</a>
    <a href="eventi.dc.html">Eventi</a>
    <a href="blog.dc.html">Blog</a>
    <a href="Home.dc.html#chisiamo">Chi siamo</a>
  </div>
  <a href="candidati.dc.html" class="nav__cta">Candidati</a>
</nav>

<header class="hero">
  <a href="corsi.dc.html" class="hero__back">← Tutti i corsi</a>
  <div class="hero__grid">
    <div>
      <span class="hero__badge {badge_cls}">{badge}</span>
      <div class="hero__eyebrow">{area}</div>
      <h1 class="hero__title">{titolo}</h1>
      <p class="hero__lead">{lead}</p>
      <div class="hero__facts">
        <div><div class="fact__k">Durata</div><div class="fact__v">{durata}</div></div>
        <div><div class="fact__k">Sede</div><div class="fact__v">Reggio Calabria</div></div>
        <div><div class="fact__k">Attestato</div><div class="fact__v">Riconosciuto</div></div>
      </div>
    </div>
    <div class="hero__media">
      <img src="{foto}" alt="{foto_alt}">
    </div>
  </div>
</header>

<main class="wrap">

  <section class="section">
    <div class="two-col">
      <div>
        <h2 class="h2">Cosa imparerai</h2>
        <ul class="checklist">
{imparerai}
        </ul>
      </div>
      <div>
        <h2 class="h2">A chi è rivolto</h2>
        <ul class="checklist">
{rivolto}
        </ul>
        <h2 class="h2" style="margin-top:44px">Sbocchi lavorativi</h2>
        <ul class="pill-list">
{sbocchi}
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <h2 class="h2">L'esperienza</h2>
    <p class="prose">{esperienza}</p>
    <div class="quote">
      <p>“{durata_dettaglio}.”</p>
    </div>{nota}
  </section>

  <section class="section">
    <h2 class="h2">In aula</h2>
    <p class="prose" style="margin-bottom:26px">Le nostre aule in Via Sbarre Inferiori 262, dove si svolge la parte teorica e laboratoriale del percorso.</p>
    <div class="gallery">
      <img src="assets/aula-audio-1.jpg" alt="Aula Genesi Lavoro" loading="lazy">
      <img src="assets/aula-audio-2.jpg" alt="Aula Genesi Lavoro" loading="lazy">
      <img src="assets/aula-audio-3.jpg" alt="Aula Genesi Lavoro" loading="lazy">
      <img src="assets/aula-audio-4.jpg" alt="Aula Genesi Lavoro" loading="lazy">
    </div>
  </section>

  <section class="section">
    <h2 class="h2">Come iscriversi</h2>
    <div class="steps">
      <div class="step">
        <div class="step__n">01</div>
        <p class="step__t">Prenota un colloquio</p>
        <p class="step__d">Gratuito e senza impegno, in sede o su Google Meet. Serve a capire se il percorso fa per te.</p>
      </div>
      <div class="step">
        <div class="step__n">02</div>
        <p class="step__t">Verifichiamo i requisiti</p>
        <p class="step__d">Controlliamo insieme se rientri in un finanziamento e quali documenti servono.</p>
      </div>
      <div class="step">
        <div class="step__n">03</div>
        <p class="step__t">Formalizzi l'iscrizione</p>
        <p class="step__d">Ti confermiamo data di avvio, calendario e modalità. Da lì si parte.</p>
      </div>
    </div>
  </section>

</main>

<section class="cta">
  <h2 class="cta__title">{cta_titolo}</h2>
  <p class="cta__sub">Parlane con la nostra segreteria: un colloquio gratuito per capire se questo è il percorso giusto per te, e come renderlo sostenibile.</p>
  <div class="cta__row">
    <a href="candidati.dc.html" class="btn btn--gold">Prenota un colloquio →</a>
    <a href="https://wa.me/390965375421" target="_blank" rel="noopener" class="btn btn--ghost">💬 Scrivici su WhatsApp</a>
  </div>
</section>

<footer class="footer">
  <div class="footer__nav">
    <a href="Home.dc.html">Home</a>
    <a href="corsi.dc.html">Corsi</a>
    <a href="finanziamenti.dc.html">Finanziamenti</a>
    <a href="eventi.dc.html">Eventi</a>
    <a href="candidati.dc.html">Candidati</a>
    <a href="lavora-con-noi.dc.html">Lavora con noi</a>
  </div>
  <p class="footer__motto">Sapere · Saper fare · Saper essere</p>
  <div class="footer__meta">Genesi Lavoro E.T.S. · P.IVA 92104080806 · Accreditamento Regione Calabria D.D. 3251/2022<br>Via Sbarre Inferiori 262, 89129 Reggio Calabria · 0965 375421</div>
</footer>

</body>
</html>
"""

CARD = """    <a href="{href}" class="card{card_mod}" data-area="{data_area}" data-tipo="{tipo}" data-formato="{formato}">
      <div class="card__photo">
        <img src="{foto}" alt="{foto_alt}" loading="lazy">
        <span class="card__badge {badge_cls}">{badge}</span>{flag}
      </div>
      <div class="card__body">
        <div class="card__meta">{area}</div>
        <h3 class="card__title">{titolo}</h3>
        <p class="card__desc">{desc}</p>
        <div class="card__foot"><span class="card__foot-durata">{durata}</span><span class="card__foot-cta">Scopri →</span></div>
      </div>
    </a>"""

NOTA = """
    <div class="nota">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
      <p>{t}</p>
    </div>"""

FLAG_PROSSIMO = '\n        <span class="card__flag">Prossimo a partire</span>'
FLAG_POSTI    = '\n        <span class="card__posti">Solo {n} posti</span>'

# I filtri di corsi.dc.html leggono data-area con questi valori esatti.
DATA_AREA = {
    "oss": "Socio-sanitario",
    "osss": "Socio-sanitario",
    "tecnico-del-suono": "Spettacolo",
    "dizione-recitazione-doppiaggio": "Spettacolo",
    "sab-somministrazione": "HoReCa",
    "amministrativo-contabile": "Amministrazione",
    "meccatronico-auto": "Meccatronica",
    "sviluppo-web": "Informatica",
    "cybersecurity": "Informatica",
    "hardware-reti": "Informatica",
    "seminario-chitarra-baglioni": "Spettacolo",
    "icdl": "Informatica",
    "eipass": "Informatica",
    "istruttore-forestale": "Forestale",
}


def build():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    corsi = data["corsi"]
    cards = []

    for c in corsi:
        badge_cls = badge_class_for(c)

        # Le voci con link_esterno hanno gia' una pagina propria (es. la landing
        # del seminario): entrano nel catalogo ma non vengono rigenerate.
        if c.get("link_esterno"):
            href = c["link_esterno"]
        else:
            href = f"corso-{c['slug']}.html"

        if not c.get("link_esterno"):
            html = PAGE.format(
                slug=c["slug"],
                titolo=esc(c["titolo"]),
                meta_desc=esc(c["meta_desc"]),
                area=esc(c["area"]),
                badge=esc(c["badge"]),
                badge_cls=badge_cls,
                durata=esc(c["durata"]),
                durata_dettaglio=esc(c["durata_dettaglio"]),
                foto=c["foto"],
                foto_alt=esc(c["foto_alt"]),
                lead=esc(c["lead"]),
                esperienza=esc(c["esperienza"]),
                cta_titolo=esc(c["cta_titolo"]),
                nota=NOTA.format(t=esc(c["nota_verifica"])) if c.get("nota_verifica") else "",
                imparerai=li_list(c["imparerai"]),
                rivolto=li_list(c["rivolto"]),
                sbocchi=li_list(c["sbocchi"]),
            )
            out = ROOT / f"corso-{c['slug']}.html"
            out.write_text(html, encoding="utf-8")
            print(f"  scritto {out.name}")
        else:
            print(f"  saltato {c['slug']} (pagina propria: {href})")

        # La descrizione breve della card e' la prima frase del lead.
        desc = c["lead"].split(". ")[0].rstrip(".") + "."
        flag = ""
        if c.get("prossimo"):
            flag += FLAG_PROSSIMO
        if c.get("posti_rimasti"):
            flag += FLAG_POSTI.format(n=c["posti_rimasti"])

        cards.append(CARD.format(
            href=href,
            card_mod=" card--prossimo" if c.get("prossimo") else "",
            formato=c.get("formato", "corso"),
            flag=flag,
            data_area=DATA_AREA[c["slug"]],
            tipo=c["tipo"],
            foto=c["foto"],
            foto_alt=esc(c["foto_alt"]),
            badge=esc(c["badge"]),
            badge_cls=badge_cls,
            area=esc(c["area"]),
            titolo=esc(c["titolo"]),
            desc=esc(desc),
            durata=esc(c["durata"]),
        ))

    # Riscrive il blocco griglia di corsi.dc.html tra i marker <div class="grid" id="grid"> e </div>
    catalogo = ROOT / "corsi.dc.html"
    src = catalogo.read_text(encoding="utf-8")
    nuovo_blocco = "\n\n".join(cards)
    pattern = re.compile(
        r'(<div class="grid" id="grid">\n).*?(\n\n    <div class="grid-empty")',
        re.DOTALL,
    )
    if not pattern.search(src):
        print("  ATTENZIONE: griglia non trovata in corsi.dc.html, link NON aggiornati")
        return
    src = pattern.sub(lambda m: m.group(1) + nuovo_blocco + m.group(2), src)
    catalogo.write_text(src, encoding="utf-8")
    print(f"  aggiornata corsi.dc.html ({len(cards)} card)")


if __name__ == "__main__":
    print("Genero le pagine corso...")
    build()
    print("Fatto.")
