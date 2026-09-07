#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspecciona colores de la imagen del logo para calibrar el recorte de fondo."""
from PIL import Image

im = Image.open(r"C:\Users\alexlocal\polaper\branding\logo-original.png").convert("RGB")
w, h = im.size
px = im.load()

def sample(x, y, label):
    # esquinas / bordes
    print(f"{label:28s} ({x:4d},{y:4d}) -> {px[x, y]}")

sample(20, 20, "esquina sup-izq")
sample(w-20, 20, "esquina sup-der")
sample(20, h-20, "esq inf-izq")
sample(w-20, h-20, "esq inf-der")
# centro-borde del squircle (fondo entre borde y arte)
sample(w//2, 8, "borde sup centro")
sample(8, h//2, "borde izq centro")
# muestra una rejilla para ver variedad de fondo
from collections import Counter
c = Counter()
for yy in range(0, h, 7):
    for xx in range(0, w, 7):
        c[px[xx, yy]] += 1
print("\nColores mas comunes (rejilla):")
for color, n in c.most_common(8):
    print(f"  {color}  x{n}")
