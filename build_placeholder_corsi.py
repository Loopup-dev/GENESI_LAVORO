#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera immagini astratte per le schede corso che non hanno una foto reale.

    python build_placeholder_corsi.py

Stessa logica del placeholder forestale gia' in uso: bande verticali sfocate,
nessun soggetto riconoscibile. Servono a non lasciare la card vuota, non a
fingere una foto: appena arriva una foto vera della vostra aula si sostituisce
il file e basta.

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
    "14-idraulico-forestale": {
        "fondo": [(58, 84, 76), (86, 116, 100)],
        "bande": [(26, 44, 42), (34, 58, 54)],
        "verso": "v",
    },
    "15-giardinaggio": {
        "fondo": [(108, 128, 78), (142, 160, 104)],
        "bande": [(58, 74, 42), (74, 92, 54)],
        "verso": "o",
    },
    "16-musica-camera": {
        "fondo": [(74, 43, 37), (110, 68, 54)],
        "bande": [(184, 146, 90), (212, 180, 130)],
        "verso": "v",
    },
    "17-orientatore-hr": {
        "fondo": [(122, 98, 88), (158, 132, 118)],
        "bande": [(74, 43, 37), (96, 62, 52)],
        "verso": "v",
    },
    "18-inclusione": {
        "fondo": [(138, 75, 58), (176, 112, 88)],
        "bande": [(92, 46, 36), (112, 60, 46)],
        "verso": "o",
    },
    "19-albo-forestale": {
        "fondo": [(70, 78, 62), (104, 114, 90)],
        "bande": [(34, 40, 32), (48, 56, 44)],
        "verso": "v",
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
