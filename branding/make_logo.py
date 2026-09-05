#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el branding Polaper: vectores Android (adaptive icon) + preview PNG + SVG.
Geometria en viewport 432 (igual que el icono de Mihon).
"""
import math, os
from PIL import Image, ImageDraw

BASE = r"C:\Users\alexlocal\polaper"
V = 432  # viewport

# Paleta pastel editorial
CREAM   = "#F9F4EA"
PINK    = "#EE8FA6"
BLUE    = "#84B6DD"
AMBER   = "#F2C078"
SKY_SOFT= "#D9E9F7"
PINK_SOFT= "#F6DCE4"
INK     = "#FFFFFFFF"

def circ(cx, cy, r):
    """pathData de un circulo (two arcs)."""
    return f"M{cx-r:.2f},{cy:.2f}a{r:.2f},{r:.2f} 0 1,0 {2*r:.2f},0a{r:.2f},{r:.2f} 0 1,0 {-2*r:.2f},0Z"

def rrect(x1, y1, x2, y2, r):
    """pathData de rectangulo redondeado."""
    return (f"M{x1+r:.2f},{y1:.2f}L{x2-r:.2f},{y1:.2f}"
            f"A{r:.2f},{r:.2f} 0 0 1 {x2:.2f},{y1+r:.2f}L{x2:.2f},{y2-r:.2f}"
            f"A{r:.2f},{r:.2f} 0 0 1 {x2-r:.2f},{y2:.2f}L{x1+r:.2f},{y2:.2f}"
            f"A{r:.2f},{r:.2f} 0 0 1 {x1:.2f},{y2-r:.2f}L{x1:.2f},{y1+r:.2f}"
            f"A{r:.2f},{r:.2f} 0 0 1 {x1+r:.2f},{y1:.2f}Z")

# --- geometria (orden de dibujo) ---
# anillo O: centro (254,200) rext=86 rint=62
ANILLO_C = (254, 200); ANILLO_RE = 86; ANILLO_RI = 62
# palo I: x 176..204, y 112..334, radio 14
PALO = (176, 112, 204, 334, 14)
# punto interior
PUNTO = (254, 200, 22)
# satelites
SAT1 = (138, 142, 17)
SAT2 = (296, 306, 23)

def ring_path(cx, cy, re, ri):
    """Anillo: circulo exterior + interior, evenOdd."""
    return circ(cx, cy, re) + circ(cx, cy, ri)

def vector_xml(inner, viewport=V):
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            f'    android:width="{viewport}dp"\n'
            f'    android:height="{viewport}dp"\n'
            f'    android:viewportWidth="{viewport}"\n'
            f'    android:viewportHeight="{viewport}">\n'
            f'{inner}</vector>\n')

def path_tag(d, fill, evenodd=False):
    fe = '        android:fillType="evenOdd"\n' if evenodd else ''
    return (f'  <path\n'
            f'      android:pathData="{d}"\n'
            f'      android:fillColor="{fill}"\n'
            f'{fe}  />\n')

# ---------- background ----------
bg_inner = (
    path_tag(f"M0,0h{V}v{V}h-{V}z", CREAM) +
    path_tag(circ(84, 84, 64), PINK_SOFT) +
    path_tag(circ(356, 356, 84), SKY_SOFT) +
    path_tag(circ(356, 80, 40), "#F3E3C9")
)
bg_xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
          '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
          f'    android:width="108dp"\n    android:height="108dp"\n'
          f'    android:viewportWidth="{V}"\n    android:viewportHeight="{V}">\n'
          f'{bg_inner}</vector>\n')

# ---------- foreground ----------
fg_inner = (
    path_tag(rrect(*PALO), BLUE) +
    path_tag(ring_path(*ANILLO_C, ANILLO_RE, ANILLO_RI), PINK, evenodd=True) +
    path_tag(circ(*PUNTO), AMBER) +
    path_tag(circ(*SAT1), SKY_SOFT) +
    path_tag(circ(*SAT2), PINK_SOFT)
)
fg_xml = vector_xml(fg_inner)

# ---------- monochrome ----------
mono_inner = (
    path_tag(rrect(*PALO), INK) +
    path_tag(circ(ANILLO_C[0], ANILLO_C[1], ANILLO_RE), INK) +
    path_tag(circ(*PUNTO), INK) +
    path_tag(circ(*SAT1), INK) +
    path_tag(circ(*SAT2), INK)
)
mono_xml = vector_xml(mono_inner)

# ---------- escribir ----------
def write(p, content):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", p)

main_draw = os.path.join(BASE, "app", "src", "main", "res", "drawable")
write(os.path.join(BASE, "app", "src", "main", "res", "drawable", "ic_launcher_background.xml"), bg_xml)
write(os.path.join(BASE, "app", "src", "main", "res", "drawable", "ic_launcher_foreground.xml"), fg_xml)
write(os.path.join(BASE, "app", "src", "main", "res", "drawable", "ic_launcher_monochrome.xml"), mono_xml)
# debug variant usa los mismos drawables
debug_draw = os.path.join(BASE, "app", "src", "debug", "res", "drawable")
write(os.path.join(debug_draw, "ic_launcher_background.xml"), bg_xml)
write(os.path.join(debug_draw, "ic_launcher_foreground.xml"), fg_xml)

# ---------- SVG logo ----------
def s_circ(cx, cy, r, fill):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
def s_rrect(x1, y1, x2, y2, r, fill):
    return f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="{r}" fill="{fill}"/>'
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {V} {V}">\n'
       f'<rect width="{V}" height="{V}" rx="96" fill="{CREAM}"/>\n'
       + s_rrect(*PALO, BLUE) + "\n"
       + f'<path fill="{PINK}" fill-rule="evenodd" d="{ring_path(*ANILLO_C, ANILLO_RE, ANILLO_RI)}"/>\n'
       + s_circ(*PUNTO, AMBER) + "\n"
       + s_circ(*SAT1, SKY_SOFT) + "\n"
       + s_circ(*SAT2, PINK_SOFT) + "\n"
       + '</svg>\n')
write(os.path.join(BASE, "branding", "logo.svg"), svg)

# ---------- PNG preview 1024 ----------
SC = 1024 / V
def px(v): return int(round(v * SC))
img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# fondo redondeado
d.rounded_rectangle([0, 0, 1023, 1023], radius=px(96), fill=CREAM)
def ell(cx, cy, r, fill):
    rr = px(r)
    d.ellipse([px(cx)-rr, px(cy)-rr, px(cx)+rr, px(cy)+rr], fill=fill)
# satelites (por detras del resto? dibujar antes)
ell(*SAT1, SKY_SOFT)
ell(*SAT2, PINK_SOFT)
# palo
d.rounded_rectangle([px(PALO[0]), px(PALO[1]), px(PALO[2]), px(PALO[3])], radius=px(PALO[4]), fill=BLUE)
# anillo: circulo rosa + agujero crema
ell(ANILLO_C[0], ANILLO_C[1], ANILLO_RE, PINK)
ell(ANILLO_C[0], ANILLO_C[1], ANILLO_RI, CREAM)
# punto
ell(*PUNTO, AMBER)
# supersample 2x para AA
img = img.resize((2048, 2048), Image.LANCZOS).resize((1024, 1024), Image.LANCZOS)
write(os.path.join(BASE, "branding", "logo-preview.png"), "")
img.save(os.path.join(BASE, "branding", "logo-preview.png"))
print("saved logo-preview.png 1024x1024")

# PNG simple para compartir fuera del repo (copia a temp)
img.save(r"C:\Users\alexlocal\AppData\Local\Temp\polaper-logo.png")
print("saved temp copy")