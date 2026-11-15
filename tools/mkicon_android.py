# Generator ikon launcher Android "SPX Express - SOC Batam" (dijalankan oleh GitHub Actions)
import os
from PIL import Image, ImageDraw, ImageFont
S = 1024
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RES = "app/src/main/res"
DENS = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}

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

def scaled(c, k):
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    inner = c.resize((int(S*k), int(S*k)), Image.LANCZOS); o = (S - inner.width) // 2
    out.alpha_composite(inner, (o, o)); return out

c = content()
fg = scaled(c, 0.56)                       # adaptive foreground (zona aman 66dp dari 108dp)
sq = Image.new("RGBA", (S, S), (0, 0, 0, 0))
m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, S-1, S-1], radius=220, fill=255)
sq.paste(gradient(), (0, 0), m); sq.alpha_composite(c)          # ikon lama (persegi membulat)
rd = Image.new("RGBA", (S, S), (0, 0, 0, 0))
m2 = Image.new("L", (S, S), 0); ImageDraw.Draw(m2).ellipse([0, 0, S-1, S-1], fill=255)
g2 = gradient(); g2.alpha_composite(scaled(c, 0.78)); rd.paste(g2, (0, 0), m2)  # ikon bulat

for name, k in DENS.items():
    d = f"{RES}/mipmap-{name}"; os.makedirs(d, exist_ok=True)
    fg.resize((int(108*k), int(108*k)), Image.LANCZOS).save(f"{d}/ic_launcher_foreground.png", optimize=True)
    sq.resize((int(48*k), int(48*k)), Image.LANCZOS).save(f"{d}/ic_launcher.png", optimize=True)
    rd.resize((int(48*k), int(48*k)), Image.LANCZOS).save(f"{d}/ic_launcher_round.png", optimize=True)
print("ikon launcher dibuat")
