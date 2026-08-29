#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera gli articoli del blog e la pagina indice da `blog-data.json`.

Uso:
    python build_blog.py

Produce `blog-<slug>.html` per ogni articolo e riscrive `blog.dc.html`.

Nota sul campo `aggiornato`: va tenuto vero. Su questo settore i concorrenti
hanno pagine ferme a bandi scaduti, e una data di revisione onesta e' il
vantaggio piu' facile da difendere.
"""

import json
import io
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "blog-data.json"

MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
        "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def data_lunga(iso):
    a, m, g = iso.split("-")
    return "%d %s %s" % (int(g), MESI[int(m) - 1], a)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


# ── blocchi del corpo ────────────────────────────────────────────────
def blocco(b):
    t, c = b["t"], b["c"]
    if t == "h2":
        return '    <h2>%s</h2>' % c
    if t == "h3":
        return '    <h3>%s</h3>' % c
    if t == "p":
        return '    <p>%s</p>' % c
    if t == "ul":
        return '    <ul>\n%s\n    </ul>' % "\n".join('      <li>%s</li>' % i for i in c)
    if t == "ol":
        return '    <ol>\n%s\n    </ol>' % "\n".join('      <li>%s</li>' % i for i in c)
    if t == "callout":
        return '    <div class="callout">%s</div>' % c
    if t == "callout-warn":
        return '    <div class="callout callout--warn">%s</div>' % c
    if t == "tabella":
        head = "".join('<th>%s</th>' % h for h in c["head"])
        rows = "".join(
            '<tr>%s</tr>' % "".join(
                ('<th scope="row">%s</th>' if i == 0 else '<td>%s</td>') % cell
                for i, cell in enumerate(r))
            for r in c["rows"])
        return ('    <div class="tbl-wrap"><table class="tbl">'
                '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (head, rows))
    if t == "fonti":
        return ('    <div class="fonti">\n'
                '      <h3 class="fonti__t">Fonti</h3>\n'
                '      <ul>\n%s\n      </ul>\n'
                '    </div>' % "\n".join('        <li>%s</li>' % f for f in c))
    return ""


STILE = """
  *{box-sizing:border-box}html,body{margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:#F7F3EC;color:#4A2B25;font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.65}
  a{color:#8A4B3A;transition:color .25s}a:hover{color:#B8925A}
  img{max-width:100%;height:auto;display:block}
  button{font-family:inherit;cursor:pointer}
  ::selection{background:#B8925A;color:#FBF8F2}
  :focus-visible{outline:2px solid #B8925A;outline-offset:3px;border-radius:6px}
  .shell{max-width:800px;margin:0 auto;padding:0 24px}

  .nav{position:sticky;top:0;z-index:900;display:flex;align-items:center;justify-content:space-between;padding:14px 40px;background:rgba(247,243,236,.93);backdrop-filter:blur(14px);border-bottom:1px solid rgba(74,43,37,.08)}
  .nav__brand{display:flex;align-items:center;gap:12px;color:#4A2B25;text-decoration:none}
  .nav__brand img{width:42px;height:42px;object-fit:contain}
  .nav__brand-name{font-family:'Playfair Display',serif;font-weight:700;font-size:18px;display:block;line-height:1}
  .nav__brand-sub{font-size:8.5px;letter-spacing:.2em;text-transform:uppercase;color:#8C8478;margin-top:3px;display:block}
  .nav__links{display:flex;gap:24px;font-size:14px;font-weight:500}
  .nav__links a{color:#4A2B25;text-decoration:none}
  .nav__links a[aria-current]{color:#8A4B3A;font-weight:600}
  .nav__cta{font-size:13px;font-weight:600;color:#FBF8F2;background:#B8925A;padding:11px 22px;border-radius:100px;text-decoration:none}
  @media(max-width:900px){.nav__links{display:none}.nav{padding:12px 20px}}

  .hero{padding:52px 0 34px}
  .crumb{font-size:13px;color:#8C8478;margin-bottom:20px}
  .crumb a{color:#8C8478;text-decoration:none}
  .eyebrow{font-size:11.5px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#B8925A;margin-bottom:15px}
  h1{font-family:'Playfair Display',serif;font-weight:700;font-size:clamp(32px,5vw,58px);line-height:1.03;letter-spacing:-.025em;margin:0 0 20px}
  .standfirst{font-size:clamp(17px,2vw,20px);line-height:1.6;color:#5c4038;margin:0 0 24px}
  .meta{font-size:13px;color:#8C8478;display:flex;gap:12px;flex-wrap:wrap;align-items:center;padding-bottom:26px;border-bottom:1px solid rgba(74,43,37,.12)}

  .updated{background:rgba(124,138,90,.12);border:1px solid rgba(124,138,90,.34);border-radius:12px;padding:14px 18px;font-size:13.5px;color:#5f6d42;margin:28px 0 0;display:flex;gap:11px;align-items:flex-start}
  .updated svg{width:18px;height:18px;flex:none;margin-top:2px}

  article h2{font-family:'Playfair Display',serif;font-weight:600;font-size:clamp(24px,3.1vw,35px);line-height:1.13;letter-spacing:-.015em;margin:48px 0 15px}
  article h3{font-family:'Playfair Display',serif;font-weight:600;font-size:clamp(19px,2.2vw,24px);line-height:1.2;margin:32px 0 11px}
  article p{font-size:17px;line-height:1.75;margin:0 0 18px}
  article ul,article ol{font-size:17px;line-height:1.75;padding-left:24px;margin:0 0 18px}
  article li{margin-bottom:9px}
  .callout{background:#FBF8F2;border-left:3px solid #B8925A;border-radius:0 14px 14px 0;padding:22px 26px;margin:26px 0}
  .callout p{margin:0 0 12px}.callout p:last-child{margin:0}
  .callout--warn{border-left-color:#8A4B3A;background:rgba(138,75,58,.07)}
  .tbl-wrap{overflow-x:auto;margin:24px 0}
  .tbl{width:100%;border-collapse:collapse;font-size:15px;min-width:520px}
  .tbl th,.tbl td{text-align:left;padding:12px 14px;border-bottom:1px solid rgba(74,43,37,.12);vertical-align:top}
  .tbl thead th{font-weight:600;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#8C8478}
  .tbl tbody th{font-weight:600;color:#4A2B25}
  .fonti{background:#FBF8F2;border:1px solid rgba(74,43,37,.12);border-radius:14px;padding:24px 26px;margin:40px 0 0}
  .fonti__t{font-family:'Inter',sans-serif !important;font-size:11.5px !important;font-weight:600 !important;letter-spacing:.16em;text-transform:uppercase;color:#8C8478;margin:0 0 12px !important}
  .fonti ul{font-size:14.5px;line-height:1.65;margin:0;padding-left:20px;color:#7a6258}
  .fonti li{margin-bottom:7px}

  .news{background:#4A2B25;color:#F7F3EC;border-radius:20px;padding:clamp(28px,4vw,42px);margin:50px 0}
  .news__t{font-family:'Playfair Display',serif;font-size:clamp(22px,2.8vw,30px);font-weight:600;line-height:1.14;margin:0 0 12px;color:#fff}
  .news__d{font-size:15.5px;line-height:1.66;color:rgba(247,243,236,.8);margin:0 0 22px}
  .news__row{display:flex;gap:10px;flex-wrap:wrap}
  .news__row input[type=email]{flex:1;min-width:210px;font-size:15px;padding:14px 16px;border:1.5px solid rgba(247,243,236,.24);border-radius:11px;background:rgba(247,243,236,.08);color:#F7F3EC;font-family:inherit}
  .news__row input[type=email]::placeholder{color:rgba(247,243,236,.45)}
  .news__row input[type=email]:focus{outline:none;border-color:#B8925A}
  .news__btn{font-size:15px;font-weight:600;color:#4A2B25;background:#B8925A;border:0;padding:14px 28px;border-radius:11px;transition:background .25s}
  .news__btn:hover{background:#D4B482}
  .news__consent{display:flex;gap:10px;align-items:flex-start;font-size:12.5px;line-height:1.55;color:rgba(247,243,236,.7);margin-top:15px}
  .news__consent input{margin-top:3px;flex:none;accent-color:#B8925A;width:16px;height:16px}
  .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}

  .altri{border-top:1px solid rgba(74,43,37,.12);padding-top:36px;margin-top:50px}
  .altri__t{font-size:11.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#8C8478;margin:0 0 20px}
  .altri__grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  @media(max-width:640px){.altri__grid{grid-template-columns:1fr}}
  .altri__c{background:#FBF8F2;border:1px solid rgba(74,43,37,.1);border-radius:14px;padding:22px;text-decoration:none;display:block;transition:transform .3s,border-color .3s}
  .altri__c:hover{transform:translateY(-3px);border-color:#B8925A}
  .altri__k{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#7C8A5A;margin-bottom:8px}
  .altri__h{font-family:'Playfair Display',serif;font-size:18px;font-weight:600;line-height:1.2;color:#4A2B25;margin:0}

  .footer{background:#4A2B25;color:#F7F3EC;padding:50px 40px 40px;text-align:center;margin-top:56px}
  .footer__nav{display:flex;flex-wrap:wrap;gap:20px;justify-content:center;margin-bottom:22px;font-size:13.5px}
  .footer__nav a{color:rgba(247,243,236,.82);text-decoration:none}
  .footer__motto{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:19px;color:#B8925A;margin:0 0 7px}
  .footer__meta{font-size:12.5px;color:rgba(247,243,236,.66);line-height:1.7}
"""

NAV = """<nav class="nav">
  <a href="Home.dc.html" class="nav__brand">
    <img src="assets/logo-transparent.png" alt="">
    <span><span class="nav__brand-name">Genesi Lavoro</span><span class="nav__brand-sub">Formazione Professionale</span></span>
  </a>
  <div class="nav__links">
    <a href="corsi.dc.html">Corsi</a>
    <a href="eventi.dc.html">Eventi</a>
    <a href="blog.dc.html"%s>Blog</a>
    <a href="docenti.dc.html">Lavora con noi</a>
    <a href="Home.dc.html#chisiamo">Chi siamo</a>
  </div>
  <a href="candidati.dc.html" class="nav__cta">Candidati</a>
</nav>"""

NEWSLETTER = """  <section class="news">
    <h2 class="news__t" style="margin-top:0">Ti avvisiamo quando esce qualcosa.</h2>
    <p class="news__d">Bandi aperti, corsi in partenza, scadenze da non perdere. Scriviamo poco e solo quando c'&egrave; davvero qualcosa da dire.</p>
    <form id="newsForm" action="/api/iscrivi-newsletter.php" method="POST" novalidate>
      <div class="hp" aria-hidden="true"><label>Non compilare<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="interessi[]" value="%s">
      <div class="news__row">
        <input type="email" name="email" required placeholder="La tua email" autocomplete="email" aria-label="La tua email">
        <button type="submit" class="news__btn" id="newsBtn">Tienimi aggiornato</button>
      </div>
      <label class="news__consent">
        <input type="checkbox" name="privacy" required>
        <span>Acconsento a ricevere aggiornamenti via email e al trattamento dei miei dati ai sensi del <strong>Reg. UE 2016/679 (GDPR)</strong>. Posso cancellarmi quando voglio.</span>
      </label>
    </form>
  </section>"""

FOOTER = """<footer class="footer">
  <div class="footer__nav">
    <a href="Home.dc.html">Home</a>
    <a href="corsi.dc.html">Corsi</a>
    <a href="eventi.dc.html">Eventi</a>
    <a href="blog.dc.html">Blog</a>
    <a href="docenti.dc.html">Lavora con noi</a>
    <a href="candidati.dc.html">Candidati</a>
  </div>
  <p class="footer__motto">Sapere &middot; Saper fare &middot; Saper essere</p>
  <div class="footer__meta">
    Genesi Lavoro E.T.S. &middot; P.IVA 92104080806 &middot; Accreditamento Regione Calabria D.D. 3251/2022<br>
    Via Sbarre Inferiori 262, 89129 Reggio Calabria &middot; 0965 375421 &middot; 393 572 6245
  </div>
</footer>"""

JS_NEWS = """<script>
(() => {
  const nf = document.getElementById('newsForm');
  if (!nf) return;
  const nb = document.getElementById('newsBtn');
  nf.addEventListener('submit', async (e) => {
    if (!nf.checkValidity()) { nf.reportValidity(); return; }
    e.preventDefault();
    nb.disabled = true; nb.textContent = 'Invio\\u2026';
    try {
      const r = await fetch(nf.action, { method:'POST', body:new FormData(nf),
        headers:{ 'Accept':'application/json','X-Requested-With':'fetch' } });
      const d = await r.json().catch(() => ({ ok:r.ok }));
      if (d.ok) { window.location.href = '/grazie.html?tipo=newsletter'; }
      else throw new Error();
    } catch (ex) {
      nb.disabled = false; nb.textContent = 'Riprova';
      alert('Non siamo riusciti a registrare l\\'iscrizione. Riprova, oppure scrivici a formazione@genesilavoro.it.');
    }
  });
})();
</script>"""


ARTICOLO = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo} | Genesi Lavoro</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://genesilavoro.it/blog-{slug}.html">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,500;0,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article",
"headline":"{titolo_esc}",
"description":"{meta_desc}",
"datePublished":"{data}","dateModified":"{aggiornato}",
"publisher":{{"@type":"EducationalOrganization","name":"Genesi Lavoro E.T.S.","url":"https://genesilavoro.it"}},
"mainEntityOfPage":"https://genesilavoro.it/blog-{slug}.html"}}
</script>
<script src="assets/analytics.js" defer></script>
<style>{stile}</style>
</head>
<body>

{nav}

<header class="hero">
  <div class="shell">
    <div class="crumb"><a href="Home.dc.html">Home</a> &rsaquo; <a href="blog.dc.html">Blog</a> &rsaquo; {categoria}</div>
    <div class="eyebrow">{occhiello}</div>
    <h1>{titolo}</h1>
    <p class="standfirst">{standfirst}</p>
    <div class="meta"><span>{data_lunga}</span><span>&middot;</span><span>{lettura} di lettura</span><span>&middot;</span><span>{categoria}</span></div>
  </div>
</header>

<div class="shell">
  <div class="updated">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 2"/></svg>
    <div><strong>Ultimo aggiornamento: {aggiornato_lungo}.</strong> Le regole su corsi e finanziamenti cambiano spesso. Prima di presentare domanda verifica sul sito ufficiale dell'ente, oppure chiamaci: la verifica te la facciamo noi, gratis.</div>
  </div>

  <article>
{corpo}
  </article>

{newsletter}

  <div class="altri">
    <p class="altri__t">Da leggere dopo</p>
    <div class="altri__grid">
{correlati}
    </div>
  </div>
</div>

{footer}
{js}
</body>
</html>
"""


INDICE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blog — corsi, bandi e finanziamenti in Calabria | Genesi Lavoro</title>
<meta name="description" content="Guide aggiornate su corsi finanziati, requisiti, qualifiche e bandi in Calabria. Scritte da un ente accreditato, con le fonti indicate.">
<link rel="canonical" href="https://genesilavoro.it/blog.dc.html">
<meta property="og:title" content="Blog — Genesi Lavoro">
<meta property="og:description" content="Guide su corsi finanziati, qualifiche e bandi in Calabria, con le fonti indicate.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,500;0,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="assets/analytics.js" defer></script>
<style>{stile}
  .shell--wide{{max-width:1180px}}
  .lista{{display:grid;gap:18px;margin:40px 0 0}}
  .post{{display:grid;grid-template-columns:auto 1fr;gap:26px;background:#FBF8F2;border:1px solid rgba(74,43,37,.1);border-radius:16px;padding:28px 30px;text-decoration:none;transition:transform .35s cubic-bezier(.16,1,.3,1),border-color .35s,box-shadow .35s}}
  .post:hover{{transform:translateY(-4px);border-color:#B8925A;box-shadow:0 16px 38px -18px rgba(74,43,37,.28)}}
  .post__n{{font-family:'Playfair Display',serif;font-size:34px;color:#B8925A;line-height:1;width:46px;flex:none}}
  .post__k{{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#7C8A5A;margin-bottom:9px}}
  .post__t{{font-family:'Playfair Display',serif;font-size:clamp(20px,2.4vw,26px);font-weight:600;line-height:1.16;color:#4A2B25;margin:0 0 9px}}
  .post__d{{font-size:15px;line-height:1.62;color:#7a6258;margin:0 0 14px}}
  .post__m{{font-size:12.5px;color:#8C8478;display:flex;gap:11px;flex-wrap:wrap;align-items:center}}
  @media(max-width:640px){{.post{{grid-template-columns:1fr;gap:12px}}.post__n{{font-size:26px}}}}
  .intro{{max-width:62ch}}
</style>
</head>
<body>

{nav}

<header class="hero">
  <div class="shell shell--wide">
    <div class="eyebrow">Blog</div>
    <h1 style="max-width:18ch">Quello che serve sapere <em style="font-style:italic;color:#8A4B3A;font-weight:500">prima</em> di iscriversi.</h1>
    <p class="standfirst intro">
      Guide su corsi finanziati, requisiti e qualifiche, scritte da chi fa formazione
      per mestiere. Con le fonti indicate e la data di ultimo aggiornamento in evidenza,
      perch&eacute; in questo settore un'informazione vecchia fa danni.
    </p>
  </div>
</header>

<div class="shell shell--wide">
  <div class="lista">
{lista}
  </div>

{newsletter}
</div>

{footer}
{js}
</body>
</html>
"""


def build():
    d = json.loads(io.open(DATA, encoding="utf-8").read())
    arts = sorted(d["articoli"], key=lambda a: a["priorita"])

    for a in arts:
        if a.get('manuale'):
            print('  saltato %s (scritto a mano)' % a['slug'])
            continue
        # correlati: i due successivi per priorita', ciclico
        i = arts.index(a)
        vicini = [arts[(i + 1) % len(arts)], arts[(i + 2) % len(arts)]]
        correlati = "\n".join(
            '      <a class="altri__c" href="blog-%s.html">\n'
            '        <div class="altri__k">%s</div>\n'
            '        <p class="altri__h">%s</p>\n'
            '      </a>' % (v["slug"], esc(v["categoria"]), esc(v["titolo_breve"]))
            for v in vicini)

        html = ARTICOLO.format(
            slug=a["slug"],
            titolo=a["titolo"],
            titolo_esc=esc(a["titolo"]),
            meta_desc=esc(a["meta_desc"]),
            categoria=esc(a["categoria"]),
            occhiello=esc(a["occhiello"]),
            standfirst=a["standfirst"],
            data=a["data"],
            data_lunga=data_lunga(a["data"]),
            aggiornato=a["aggiornato"],
            aggiornato_lungo=data_lunga(a["aggiornato"]),
            lettura=a["lettura"],
            corpo="\n".join(blocco(b) for b in a["corpo"]),
            stile=STILE,
            nav=NAV % "",
            newsletter=NEWSLETTER % esc(a["categoria"]),
            correlati=correlati,
            footer=FOOTER,
            js=JS_NEWS,
        )
        out = ROOT / ("blog-%s.html" % a["slug"])
        io.open(out, "w", encoding="utf-8").write(html)
        print("  scritto %s" % out.name)

    # ── indice ──
    voci = []
    for n, a in enumerate(arts, 1):
        voci.append(
            '    <a class="post" href="blog-%s.html">\n'
            '      <div class="post__n">%02d</div>\n'
            '      <div>\n'
            '        <div class="post__k">%s</div>\n'
            '        <h2 class="post__t">%s</h2>\n'
            '        <p class="post__d">%s</p>\n'
            '        <div class="post__m"><span>Aggiornato il %s</span><span>&middot;</span><span>%s</span></div>\n'
            '      </div>\n'
            '    </a>' % (a["slug"], n, esc(a["categoria"]), esc(a["titolo"]),
                          a["standfirst"], data_lunga(a["aggiornato"]), a["lettura"]))

    idx = INDICE.format(
        stile=STILE,
        nav=NAV % ' aria-current="page"',
        lista="\n".join(voci),
        newsletter=NEWSLETTER % "Generale",
        footer=FOOTER,
        js=JS_NEWS,
    )
    io.open(ROOT / "blog.dc.html", "w", encoding="utf-8").write(idx)
    print("  aggiornata blog.dc.html (%d articoli)" % len(arts))


if __name__ == "__main__":
    print("Genero il blog...")
    build()
    print("Fatto.")
