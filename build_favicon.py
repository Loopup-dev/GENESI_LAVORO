#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera il set di favicon da assets/logo-transparent.png.

    python build_favicon.py

PERCHE' DUE VERSIONI DIVERSE
Il logo intero ha il testo curvo attorno ("Sapere / Saper fare / Saper essere")
e una chioma di fiori chiari su fondo crema. Sotto i 100px quel testo diventa
rumore e la chioma sparisce per mancanza di contrasto: provato, a 16px si vede
una macchia beige.

Quindi:
  - fino a 96px  -> silhouette piena dell'albero, marrone brand su crema.
                    La sagoma si ricava dal canale alpha, dilatata per fondere
                    i singoli petali in una chioma unica. A 16px si legge.
  - da 180px in su -> marchio completo a colori (albero + libro), che a quella
                    dimensione ha spazio per essere sé stesso.

Google usa il favicon per il risultato di ricerca e lo vuole quadrato e
multiplo di 48px. Il file /favicon.ico deve stare in radice: e' il percorso
che il crawler prova per primo.
"""

from PIL import Image, ImageFilter
from pathlib import Path

ROOT = Path(__file__).parent
SRG = ROOT / "assets" / "logo-transparent.png"

CREMA = (247, 243, 236, 255)   # #F7F3EC, fondo del sito
BRUNO = (74, 43, 37, 255)      # #4A2B25, marrone del brand

# Riquadri ricavati analizzando il canale alpha del logo:
# la corona di testo sta fuori da queste coordinate.
ALBERO = (205, 118, 600, 690)   # chioma + tronco, senza libro
MARCHIO = (98, 121, 680, 786)   # albero + libro, senza testo


def silhouette(lato):
    """Sagoma piena dell'albero: legge anche a 16px."""
    src = Image.open(SRG).convert("RGBA")
    alb = src.crop(ALBERO)
    a = alb.split()[3].point(lambda v: 255 if v > 40 else 0)
    a = a.filter(ImageFilter.MaxFilter(21))   # fonde i petali
    a = a.filter(ImageFilter.MinFilter(13))   # richiude la sagoma
    n = max(alb.size)
    aria = int(n * 0.10)
    tela = Image.new("RGBA", (n + aria * 2, n + aria * 2), CREMA)
    sag = Image.new("RGBA", alb.size, BRUNO)
    sag.putalpha(a)
    tela.alpha_composite(sag, ((tela.size[0] - alb.size[0]) // 2,
                               (tela.size[1] - alb.size[1]) // 2))
    return tela.resize((lato, lato), Image.LANCZOS)


def completo(lato):
    """Marchio a colori, per le misure grandi."""
    src = Image.open(SRG).convert("RGBA")
    m = src.crop(MARCHIO)
    n = max(m.size)
    aria = int(n * 0.07)
    tela = Image.new("RGBA", (n + aria * 2, n + aria * 2), CREMA)
    tela.alpha_composite(m, ((tela.size[0] - m.size[0]) // 2,
                             (tela.size[1] - m.size[1]) // 2))
    return tela.resize((lato, lato), Image.LANCZOS)


def build():
    ass = ROOT / "assets"

    # .ico multi-risoluzione in radice: e' quello che cerca il crawler
    ico = ROOT / "favicon.ico"
    silhouette(256).save(ico, format="ICO",
                         sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("  scritto favicon.ico (16/32/48/64)")

    for lato in (48, 96, 192):
        p = ass / ("favicon-%d.png" % lato)
        silhouette(lato).save(p, optimize=True)
        print("  scritto %s" % p.name)

    completo(180).convert("RGB").save(ass / "apple-touch-icon.png",
                                      optimize=True)
    print("  scritto apple-touch-icon.png (180, marchio completo)")

    completo(512).save(ass / "icon-512.png", optimize=True)
    print("  scritto icon-512.png (marchio completo)")


if __name__ == "__main__":
    print("Genero le favicon...")
    build()
    print("Fatto.")
