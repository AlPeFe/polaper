#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los iconos del launcher Android a partir del logo oficial (imagen completa).
Foreground = logo centrado al 84% (margen de seguridad para la mascara del launcher).
Background = color oscuro del fondo de la imagen.
Monochrome = silueta blanca (themed icons Android 13+).
"""
import os
from PIL import Image, ImageOps

BASE = r"C:\Users\alexlocal\polaper"
SRC = os.path.join(BASE, "branding", "logo-original.png")
RES = os.path.join(BASE, "app", "src", "main", "res")

im = Image.open(SRC).convert("RGBA")

# ---- color del fondo exterior (esquinas): negro; squircle ~ #110F18
# Detectamos el color medio del borde exterior para el background
px = im.load()
w, h = im.size
corners = [px[5, 5], px[w - 6, 5], px[5, h - 6], px[w - 6, h - 6]]
r = sum(c[0] for c in corners) // 4
g = sum(c[1] for c in corners) // 4
b = sum(c[2] for c in corners) // 4
bg_hex = "#{:02X}{:02X}{:02X}".format(r, g, b)
print("Color fondo exterior (esquinas):", bg_hex, (r, g, b))

# ---- foreground: logo centrado al 84% en canvas cuadrado
CANVAS = 432  # xxxhdpi: 108dp * 4
TARGET = int(CANVAS * 0.84)
art = ImageOps.fit(im, (TARGET, TARGET), Image.LANCZOS)

def paste_centered(base_size, img):
    canvas = Image.new("RGBA", (base_size, base_size), (0, 0, 0, 0))
    s = int(base_size * 0.84)
    img_s = img.resize((s, s), Image.LANCZOS)
    canvas.paste(img_s, ((base_size - s) // 2, (base_size - s) // 2), img_s)
    return canvas

# ---- monochrome: silueta blanca (umbral de luminancia) sobre el arte
def make_monochrome(img_rgba):
    gray = img_rgba.convert("L")
    alpha = img_rgba.getchannel("A")
    # Umbral: pixeles claros (piel/rosa/blanco/paginas) -> blanco; oscuros (fondo/pelo) -> transparente
    mask = gray.point(lambda v: 255 if v > 60 else 0)
    mask = mask.convert("L")
    out = Image.new("RGBA", img_rgba.size, (255, 255, 255, 0))
    out.putalpha(mask)
    return out

mono = make_monochrome(im)

# ---- escribir PNGs por densidad (foreground + monochrome)
densities = {
    "mdpi": 108,
    "hdpi": 162,
    "xhdpi": 216,
    "xxhdpi": 324,
    "xxxhdpi": 432,
}
for dpi, size in densities.items():
    d = os.path.join(RES, f"drawable-{dpi}")
    os.makedirs(d, exist_ok=True)
    fg = paste_centered(size, im)
    fg.save(os.path.join(d, "ic_launcher_foreground.png"))
    mo = paste_centered(size, mono)
    mo.save(os.path.join(d, "ic_launcher_monochrome.png"))
    print(f"drawable-{dpi}: foreground + monochrome {size}px")

# ---- reescribir background como vector de color solido del fondo
bg_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
  <path
      android:pathData="M0,0h108v108h-108z"
      android:fillColor="{bg_hex}"/>
</vector>
'''
main_drawable = os.path.join(RES, "drawable", "ic_launcher_background.xml")
with open(main_drawable, "w", encoding="utf-8") as f:
    f.write(bg_xml)
print("background.xml ->", bg_hex)

# preview para verificacion
prev = paste_centered(512, im)
prev.save(os.path.join(BASE, "branding", "launcher-preview.png"))
print("preview guardado en branding/launcher-preview.png")
