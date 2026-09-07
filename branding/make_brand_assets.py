#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assets finales de marca Polaper: small icon de notificacion (silueta blanca)
y splash (logo completo). Elimina ic_mihon*."""
import os
from PIL import Image

BASE = r"C:\Users\alexlocal\polaper"
SRC = os.path.join(BASE, "branding", "logo-original.png")
RES = os.path.join(BASE, "app", "src", "main", "res")

im = Image.open(SRC).convert("RGBA")

# Silueta blanca (monocromo) a partir del arte: umbral de luminancia
def make_monochrome(img_rgba):
    gray = img_rgba.convert("L")
    mask = gray.point(lambda v: 255 if v > 60 else 0).convert("L")
    out = Image.new("RGBA", img_rgba.size, (255, 255, 255, 0))
    out.putalpha(mask)
    return out

mono_full = make_monochrome(im)

# Recortar a contenido (bbox del arte) para que la silueta llene el small icon
def trim(img):
    bbox = img.getchannel("A").getbbox()
    if bbox:
        return img.crop(bbox)
    return img

mono = trim(mono_full)
# centrar el arte en canvas cuadrado
w, h = mono.size
side = max(w, h)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(mono, ((side - w) // 2, (side - h) // 2), mono)
mono = canvas

# small icon notificacion: 24dp por densidad (silueta blanca con algo de padding)
notif_sizes = {"mdpi": 24, "hdpi": 36, "xhdpi": 48, "xxhdpi": 72, "xxxhdpi": 96}
for dpi, size in notif_sizes.items():
    d = os.path.join(RES, f"drawable-{dpi}")
    os.makedirs(d, exist_ok=True)
    # arte al 80% del canvas para que respire
    inner = mono.resize((int(size * 0.8), int(size * 0.8)), Image.LANCZOS)
    c = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    c.paste(inner, ((size - inner.width) // 2, (size - inner.height) // 2), inner)
    c.save(os.path.join(d, "ic_notification.png"))
    print(f"ic_notification {dpi} {size}px")

# splash: logo completo a 512px en drawable-nodpi
nodpi = os.path.join(RES, "drawable-nodpi")
os.makedirs(nodpi, exist_ok=True)
splash = im.resize((512, 512), Image.LANCZOS)
splash.save(os.path.join(nodpi, "ic_splash.png"))
print("ic_splash.png 512px en drawable-nodpi")

# limpiar assets viejos de la marca Mihon
for p in [
    os.path.join(RES, "drawable", "ic_mihon.xml"),
    os.path.join(RES, "drawable", "ic_mihon_splash.xml"),
]:
    if os.path.exists(p):
        os.remove(p)
        print("borrado", os.path.basename(p))

# preview de la silueta
mono_small = mono.resize((128, 128), Image.LANCZOS)
mono_small.save(os.path.join(BASE, "branding", "notification-preview.png"))
print("preview silueta en branding/notification-preview.png")
