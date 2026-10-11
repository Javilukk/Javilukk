"""Genera el banner pixel-art (naranja) del perfil.
Uso: python make_banner.py "Martin Javier" "ML / DATA SCIENCE  ·  MECHATRONICS ENGINEERING" assets/banner.svg
El nombre se parte en 2 líneas si tiene 2-3 palabras; el subtítulo se parte en el '·'.
"""
import os
import random
import sys
import unicodedata

NAME = sys.argv[1] if len(sys.argv) > 1 else "TU NOMBRE"
SUB = sys.argv[2] if len(sys.argv) > 2 else "ML / DATA SCIENCE  ·  MECHATRONICS ENGINEERING"
OUT = sys.argv[3] if len(sys.argv) > 3 else "banner.svg"
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)

W = 800
BG, CREAM, MUTED, OR = "#0d1117", "#e6e0d4", "#8b949e", "#f0883e"
ORANGES = ["#4a2308", "#8a3f0a", "#d9680f", "#f0883e", "#ffb067"]
ACCENTS = ["#ffd8a8", CREAM, "#ffcc66"]

FONT = {
"A":"01110 10001 10001 11111 10001 10001 10001","B":"11110 10001 10001 11110 10001 10001 11110",
"C":"01110 10001 10000 10000 10000 10001 01110","D":"11110 10001 10001 10001 10001 10001 11110",
"E":"11111 10000 10000 11110 10000 10000 11111","F":"11111 10000 10000 11110 10000 10000 10000",
"G":"01110 10001 10000 10111 10001 10001 01111","H":"10001 10001 10001 11111 10001 10001 10001",
"I":"01110 00100 00100 00100 00100 00100 01110","J":"00111 00010 00010 00010 00010 10010 01100",
"K":"10001 10010 10100 11000 10100 10010 10001","L":"10000 10000 10000 10000 10000 10000 11111",
"M":"10001 11011 10101 10101 10001 10001 10001","N":"10001 11001 10101 10011 10001 10001 10001",
"O":"01110 10001 10001 10001 10001 10001 01110","P":"11110 10001 10001 11110 10000 10000 10000",
"Q":"01110 10001 10001 10001 10101 10010 01101","R":"11110 10001 10001 11110 10100 10010 10001",
"S":"01111 10000 10000 01110 00001 00001 11110","T":"11111 00100 00100 00100 00100 00100 00100",
"U":"10001 10001 10001 10001 10001 10001 01110","V":"10001 10001 10001 10001 10001 01010 00100",
"W":"10001 10001 10001 10101 10101 11011 10001","X":"10001 10001 01010 00100 01010 10001 10001",
"Y":"10001 10001 01010 00100 00100 00100 00100","Z":"11111 00001 00010 00100 01000 10000 11111",
"0":"01110 10011 10101 10101 10101 11001 01110","1":"00100 01100 00100 00100 00100 00100 01110",
"2":"01110 10001 00001 00110 01000 10000 11111","3":"11110 00001 00001 01110 00001 00001 11110",
"4":"10010 10010 10010 11111 00010 00010 00010","5":"11111 10000 11110 00001 00001 10001 01110",
"6":"01110 10000 10000 11110 10001 10001 01110","7":"11111 00001 00010 00100 01000 01000 01000",
"8":"01110 10001 10001 01110 10001 10001 01110","9":"01110 10001 10001 01111 00001 00001 01110",
" ":"00000 00000 00000 00000 00000 00000 00000","-":"00000 00000 00000 11111 00000 00000 00000",
".":"00000 00000 00000 00000 00000 01100 01100","_":"00000 00000 00000 00000 00000 00000 11111",
}


def clean(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").upper()


words = clean(NAME).split()
lines = words if 2 <= len(words) <= 3 else [clean(NAME)]
longest = max(len(l) * 6 - 1 for l in lines)
cell = max(4, min(10, 400 // longest))
x0, y0, gap = 40, 40, 14
name_h = len(lines) * 7 * cell + (len(lines) - 1) * gap

sub_lines = [p.strip() for p in SUB.split("·")]
y_sub = y0 + name_h + 46
last_sub = y_sub + 32 * (len(sub_lines) - 1)
bar_y = last_sub + 28
H = bar_y + 4 + 30

rnd = random.Random(42)
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}">',
       f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>']

mx, size = 480, 20
cols, rows = (W - mx) // size, H // size
for r in range(rows):
    for c in range(cols):
        if rnd.random() < (c / cols) ** 0.9 * 0.85:
            color = rnd.choice(ACCENTS) if rnd.random() < 0.07 else rnd.choice(ORANGES[1:] if c > cols * 0.4 else ORANGES)
            x, y = mx + c * size, r * size
            if rnd.random() < 0.06:
                out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}"><animate attributeName="opacity" values="1;0.25;1" dur="{rnd.uniform(2,5):.1f}s" repeatCount="indefinite"/></rect>')
            else:
                out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}"/>')

for li, text in enumerate(lines):
    ly = y0 + li * (7 * cell + gap)
    for i, ch in enumerate(text):
        glyph = FONT.get(ch, FONT[" "]).split()
        for ry, row in enumerate(glyph):
            for rx, bit in enumerate(row):
                if bit == "1":
                    out.append(f'<rect x="{x0 + (i*6 + rx)*cell}" y="{ly + ry*cell}" width="{cell}" height="{cell}" fill="{CREAM}"/>')

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
for i, t in enumerate(sub_lines):
    out.append(f'<text x="{x0}" y="{y_sub + 32*i}" font-family="{MONO}" font-size="22" textLength="{len(t)*14}" lengthAdjust="spacing" fill="{MUTED}">{t}</text>')
cx = x0 + len(sub_lines[-1]) * 14 + 8
out.append(f'<rect x="{cx}" y="{last_sub-18}" width="11" height="22" fill="{OR}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
out.append(f'<rect x="{x0}" y="{bar_y}" width="120" height="4" fill="{OR}"/><rect x="{x0+130}" y="{bar_y}" width="40" height="4" fill="#8a3f0a"/><rect x="{x0+180}" y="{bar_y}" width="20" height="4" fill="#4a2308"/>')
out.append("</svg>")
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("banner:", OUT, f"{W}x{H}", "celda", cell)
