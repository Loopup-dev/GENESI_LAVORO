# -*- coding: utf-8 -*-
"""
Scarica le immagini generate per i corsi nuovi e le porta al formato delle
altre foto corso: 1200x900 JPEG progressivo, qualita' calata finche' il file
non scende sotto i 160 KB.

    python build_foto_corsi.py

Immagini generate con Higgsfield (modello z_image), settembre 2026. Gli URL
CloudFront qui sotto scadono: se lo rilanci fra mesi e ti da 403, le foto sono
gia' in assets/corsi/ e non serve rifare nulla. Lo script resta per tracciare
da dove vengono.

Il crop di 15-giardinaggio non e' centrato apposta: taglia fuori un artefatto
del generatore (un secondo paio di cesoie sovrapposto al primo) che restava
nella meta' alta a destra.

Manca 18-inclusione: la generazione e' fallita per crediti esauriti, quella
card usa ancora il placeholder astratto di build_placeholder_corsi.py.

NON usare queste immagini su Google Business: li' le foto devono ritrarre
l'attivita' reale. Per quello valgono solo le aula-audio-*.jpg.
"""
import urllib.request, io
from pathlib import Path
from PIL import Image

OUT = Path("assets/corsi")
W, H = 1200, 900
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3GECVYAK5DejXSCGg7t6VwsulDn/"

# nome -> (file remoto, riquadro da ritagliare sull'originale 2048x1536)
IMG = {
    "14-idraulico-forestale": ("hf_20260908_133353_7aaf315b-14d4-4c31-9509-cda3da56bd1c.png", None),
    "15-giardinaggio":        ("hf_20260908_133328_d529abcd-1e66-49b9-8ed0-341911f575a1.png", (427, 734, 1497, 1536)),
    "16-musica-camera":       ("hf_20260908_133430_9117e043-2392-466c-b5f5-533576f665e7.png", None),
    "17-orientatore-hr":      ("hf_20260908_133706_d5a18448-228b-4452-a0c5-3a95f2130ad7.png", None),
    "20-abbattimento-base":   ("hf_20260908_133353_d3c21a67-275d-4d00-930a-3888be5ca212.png", None),
}


def riempi(im):
    """Porta a 1200x900 senza deformare: scala sul lato corto e centra."""
    r = max(W / im.width, H / im.height)
    n = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    sx, sy = (n.width - W) // 2, (n.height - H) // 2
    return n.crop((sx, sy, sx + W, sy + H))


def salva(im, dove, tetto=160_000):
    """Scende di qualita' finche' il file non sta sotto il tetto in byte."""
    for q in (84, 80, 76, 72, 68):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= tetto or q == 68:
            dove.write_bytes(buf.getvalue())
            return buf.tell() // 1024, q


for nome, (file_remoto, riquadro) in IMG.items():
    req = urllib.request.Request(BASE + file_remoto, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        im = Image.open(io.BytesIO(r.read())).convert("RGB")
    if riquadro:
        im = im.crop(riquadro)
    peso, q = salva(riempi(im), OUT / (nome + ".jpg"))
    print("  %-24s %3d KB  (q%d)" % (nome + ".jpg", peso, q))
print("Fatto.")
