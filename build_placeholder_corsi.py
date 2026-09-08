#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera l'immagine astratta per le schede corso che non hanno ancora una foto.

    python build_placeholder_corsi.py

Bande verticali sfocate, nessun soggetto riconoscibile. Serve a non lasciare
la card vuota, non a fingere una foto: appena arriva una foto vera si
sostituisce il file e basta.

ATTENZIONE: qui sotto deve restare SOLO chi e' ancora senza foto. Gli altri
corsi nuovi (14, 15, 16, 17, 19) hanno ora immagini vere generate da
build_foto_corsi.py: se li rimetti in GAMME, al primo lancio le sovrascrivi.

NON usare queste immagini su Google Business: li' le foto devono ritrarre
l'attivita' reale.
"""

from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import random

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "corsi"
W, H = 1200, 900

# Ogni corso ha la sua gamma: due toni scuri per le bande, due chiari per il fondo.
GAMME = {
    "18-inclusione": {
        "fondo": [(138, 75, 58), (176, 112, 88)],
        "bande": [(92, 46, 36), (112, 60, 46)],
        "verso": "o",
    },
}


def sfuma(dis, c1, c2, verso):
    """Fondo a gradiente."""
    n = H if verso == "o" else W
    for i in range(n):
        t = i / n
        col = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        if verso == "o":
            dis.line([(0, i), (W, i)], fill=col)
        else:
            dis.line([(i, 0), (i, H)], fill=col)


def genera(nome, g, seme):
    rnd = random.Random(seme)
    im = Image.new("RGB", (W, H))
    dis = ImageDraw.Draw(im)
    sfuma(dis, g["fondo"][0], g["fondo"][1], g["verso"])

    # bande di larghezza e posizione irregolari
    pos = 0
    lungo = W if g["verso"] == "v" else H
    while pos < lungo:
        salto = rnd.randint(int(lungo * 0.06), int(lungo * 0.16))
        largo = rnd.randint(int(lungo * 0.008), int(lungo * 0.035))
        pos += salto
        if pos >= lungo:
            break
        col = g["bande"][rnd.randint(0, 1)]
        if g["verso"] == "v":
            dis.rectangle([pos, 0, pos + largo, H], fill=col)
        else:
            dis.rectangle([0, pos, W, pos + largo], fill=col)

    im = im.filter(ImageFilter.GaussianBlur(radius=rnd.randint(9, 15)))
    im.save(OUT / (nome + ".jpg"), quality=86, optimize=True)
    return nome


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print("Genero i placeholder...")
    for i, (nome, g) in enumerate(GAMME.items()):
        print("  scritto %s.jpg" % genera(nome, g, 40 + i * 7))
    print("Fatto.")
