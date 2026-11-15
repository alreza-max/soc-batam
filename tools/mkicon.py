# Generator ikon PWA "SPX Express - SOC Batam" (dijalankan oleh GitHub Actions)
import os
from PIL import Image, ImageDraw, ImageFont
S = 1024
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT = "icons"

def gradient():
    g = Image.new("RGBA", (S, S)); d = ImageDraw.Draw(g)
    for y in range(S):
        t = y / S
        d.line([(0, y), (S, y)], fill=(int(0xF5*(1-t)+0xD7*t), int(0x5A*(1-t)+0x3A*t), int(0x2E*(1-t)+0x1F*t), 255))
    return g

def ctext(d, txt, y, maxw, size):
    while True:
        f = ImageFont.truetype(FB, size); bb = d.textbbox((0, 0), txt, font=f)
        if bb[2] - bb[0] <= maxw: break
        size -= 4
    d.text(((S - (bb[2] - bb[0])) / 2 - bb[0], y - bb[1]), txt, font=f, fill=(255, 255, 255, 255))

def content():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    ctext(d, "SPX Express", 120, 820, 150)
    d.rounded_rectangle([432, 272, 592, 282], radius=5, fill=(255, 255, 255, 170))
    cx, cy, w, h, dep = S // 2, 425, 165, 95, 165
    top = [(cx, cy-h), (cx+w, cy), (cx, cy+h), (cx-w, cy)]
    left = [(cx-w, cy), (cx, cy+h), (cx, cy+h+dep), (cx-w, cy+dep)]
    right = [(cx+w, cy), (cx, cy+h), (cx, cy+h+dep), (cx+w, cy+dep)]
    d.polygon(top, fill=(255, 255, 255, 255)); d.polygon(left, fill=(255, 236, 226, 255)); d.polygon(right, fill=(255, 214, 196, 255))
    tw = 28
    d.polygon([(cx-w/2-tw, cy-h/2), (cx-w/2+tw, cy-h/2), (cx+w/2+tw, cy+h/2), (cx+w/2-tw, cy+h/2)], fill=(238, 77, 45, 255))
    d.polygon([(cx+w/2-tw, cy+h/2), (cx+w/2+tw, cy+h/2), (cx+w/2+tw, cy+h/2+dep*0.45), (cx+w/2-tw, cy+h/2+dep*0.45)], fill=(238, 77, 45, 230))
    for p in (top, left, right): d.line(p + [p[0]], fill=(190, 50, 25, 255), width=7, joint="curve")
    ctext(d, "SOC Batam", 755, 840, 170)
    return img

os.makedirs(OUT, exist_ok=True)
c = content()
# ikon "any": sudut membulat transparan
mask = Image.new("L", (S, S), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, S-1, S-1], radius=220, fill=255)
anyi = Image.new("RGBA", (S, S), (0, 0, 0, 0)); anyi.paste(gradient(), (0, 0), mask); anyi.alpha_composite(c)
for s in (192, 512): anyi.resize((s, s), Image.LANCZOS).save(f"{OUT}/icon-{s}.png", optimize=True)
# ikon "maskable": latar penuh, konten di zona aman
mk = gradient(); inner = c.resize((int(S*0.74), int(S*0.74)), Image.LANCZOS); o = (S - inner.width) // 2
mk.alpha_composite(inner, (o, o))
mk.resize((512, 512), Image.LANCZOS).save(f"{OUT}/maskable-512.png", optimize=True)
mk.resize((180, 180), Image.LANCZOS).convert("RGB").save(f"{OUT}/apple-touch-icon.png", optimize=True)
print("ikon dibuat")
