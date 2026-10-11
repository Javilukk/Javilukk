"""Genera los SVG del perfil (EN y ES) en ./assets
Uso:  python make_assets.py      (necesita make_banner.py en la misma carpeta)

Diseño pensado para leerse bien en celular: lienzo de 600 px, textos grandes.
Para mostrar más proyectos/hitos, edita KEEP_CARDS y KEEP_JOURNEY más abajo.
"""
import math
import os
import random
import subprocess
import sys
from xml.sax.saxutils import escape as esc

NAME = "Martin Javier"
W = 600

BG, CARD, CARD2, BORDER = "#0d1117", "#161b22", "#21262d", "#30363d"
OR, OR1, OR2, OR3, OR4 = "#f0883e", "#ffb067", "#d9680f", "#8a3f0a", "#4a2308"
TXT, SOFT, MUTED = "#e6edf3", "#c9d1d9", "#8b949e"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def wrap(w, h, body, title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}">{body}</svg>')


def save(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def pulse(cx, cy, r0=5, r1=14, dur=2):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{OR}" stroke-width="1.5">'
            f'<animate attributeName="r" values="{r0};{r1}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.8;0" dur="{dur}s" repeatCount="indefinite"/></circle>')


def section(num, title):
    h = 50
    x_line = 44 + len(title) * 15 + 16
    body = (f'<text x="0" y="34" font-family="{MONO}" font-size="15" fill="{OR}">{num}</text>'
            f'<text x="44" y="35" font-family="{SANS}" font-size="26" font-weight="700" fill="{TXT}">{esc(title)}</text>'
            f'<line x1="{x_line}" y1="25" x2="{W}" y2="25" stroke="{BORDER}"/>'
            f'<rect x="{x_line}" y="24" width="48" height="2" fill="{OR}"/>')
    return wrap(W, h, body, title)


def chip(x, y, text, fs=13.5):
    w = len(text) * fs * 0.6 + 26
    return (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="30" rx="15" fill="{CARD2}" stroke="{BORDER}"/>'
            f'<text x="{x + w/2:.1f}" y="{y+20}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" fill="{MUTED}">{esc(text)}</text>'), w


S = f'fill="none" stroke="{OR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'


def ic_chart():
    return (f'<polyline {S} points="8,29 15,21 21,25 32,11"/><circle cx="32" cy="11" r="2.5" fill="{OR}"/>'
            f'<line {S} x1="8" y1="34" x2="32" y2="34" opacity=".4"/>')


def ic_spec():
    return f'<polyline {S} points="6,30 12,30 15,16 18,30 22,30 25,9 28,30 34,30"/>'


def ic_sun():
    rays = "".join(
        f'<line {S} x1="{20+10*math.cos(a):.1f}" y1="{20+10*math.sin(a):.1f}" x2="{20+14*math.cos(a):.1f}" y2="{20+14*math.sin(a):.1f}"/>'
        for a in [i * math.pi / 4 for i in range(8)])
    return f'<circle {S} cx="20" cy="20" r="6"/>' + rays


def ic_search():
    return (f'<circle {S} cx="18" cy="18" r="9"/><line {S} x1="25" y1="25" x2="33" y2="33"/>'
            f'<circle cx="18" cy="18" r="2.5" fill="{OR}"/>')


def ic_gear():
    return (f'<circle {S} cx="20" cy="20" r="8"/><circle cx="20" cy="20" r="3" fill="{OR}"/>'
            f'<circle cx="20" cy="20" r="12" fill="none" stroke="{OR}" stroke-width="4" stroke-dasharray="3.14 3.14"/>')


def ic_text():
    return (f'<line {S} x1="9" y1="12" x2="31" y2="12"/><line {S} x1="9" y1="20" x2="26" y2="20"/>'
            f'<line {S} x1="9" y1="28" x2="31" y2="28"/>')


ICONS = {"chart": ic_chart, "spec": ic_spec, "sun": ic_sun, "search": ic_search, "gear": ic_gear, "text": ic_text}


def card(icon, title, sub, desc, tags, metrics=None):
    has_m = bool(metrics)
    h = 322 if has_m else 228
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="16" fill="{CARD}" stroke="{BORDER}"/>',
         f'<rect x="24" y="0" width="44" height="3" rx="1.5" fill="{OR}"/>',
         f'<rect x="24" y="26" width="52" height="52" rx="12" fill="{CARD2}"/>',
         f'<g transform="translate(30,32)">{ICONS[icon]()}</g>',
         f'<text x="94" y="52" font-family="{SANS}" font-size="22" font-weight="700" fill="{TXT}">{esc(title)}</text>',
         f'<text x="94" y="74" font-family="{MONO}" font-size="14" fill="{MUTED}">{esc(sub)}</text>',
         f'<text x="{W-28}" y="52" text-anchor="end" font-family="{SANS}" font-size="22" fill="{OR}">↗</text>']
    for i, line in enumerate(desc):
        b.append(f'<text x="24" y="{122 + i*25}" font-family="{SANS}" font-size="16.5" fill="{SOFT}">{esc(line)}</text>')
    x = 24
    for t in tags:
        c, cw = chip(x, 172, t)
        b.append(c)
        x += cw + 8
    if has_m:
        bw = (W - 48 - 20) / 3
        for i, (num, label) in enumerate(metrics):
            bx = 24 + i * (bw + 10)
            b.append(f'<rect x="{bx:.1f}" y="224" width="{bw:.1f}" height="76" rx="12" fill="#2a1a0d" stroke="{OR3}"/>'
                     f'<text x="{bx + bw/2:.1f}" y="262" text-anchor="middle" font-family="{SANS}" font-size="32" font-weight="700" fill="{OR1}">{esc(num)}</text>'
                     f'<text x="{bx + bw/2:.1f}" y="285" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{MUTED}">{esc(label)}</text>')
    return wrap(W, h, "".join(b), title)


def stats(items):
    h = 118
    colw = W / 4
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="16" fill="{CARD}" stroke="{BORDER}"/>']
    for i, (big, l1, l2) in enumerate(items):
        cx = colw * i + colw / 2
        b.append(f'<text x="{cx}" y="54" text-anchor="middle" font-family="{SANS}" font-size="25" font-weight="700" fill="{OR}">{esc(big)}</text>')
        b.append(f'<text x="{cx}" y="80" text-anchor="middle" font-family="{SANS}" font-size="13.5" fill="{MUTED}">{esc(l1)}</text>')
        b.append(f'<text x="{cx}" y="98" text-anchor="middle" font-family="{SANS}" font-size="13.5" fill="{MUTED}">{esc(l2)}</text>')
        if i:
            b.append(f'<line x1="{colw*i}" y1="24" x2="{colw*i}" y2="{h-24}" stroke="{BORDER}"/>')
    return wrap(W, h, "".join(b), "stats")


def about(filename, rows):
    top, rowh = 48, 36
    h = top + len(rows) * rowh + 26
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="16" fill="{CARD}" stroke="{BORDER}"/>',
         f'<circle cx="28" cy="24" r="5.5" fill="{OR4}"/><circle cx="47" cy="24" r="5.5" fill="{OR3}"/><circle cx="66" cy="24" r="5.5" fill="{OR}"/>',
         f'<text x="92" y="29" font-family="{MONO}" font-size="13" fill="{MUTED}">{esc(filename)}</text>',
         f'<line x1="0" y1="{top}" x2="{W}" y2="{top}" stroke="{BORDER}"/>']
    for i, (k, v) in enumerate(rows):
        y = top + 36 + i * rowh
        b.append(f'<text x="28" y="{y}" font-family="{MONO}" font-size="14" fill="{MUTED}">{esc(k)}</text>')
        if i == len(rows) - 1:
            b.append(f'<circle cx="147" cy="{y-5}" r="4.5" fill="{OR}"/>{pulse(147, y-5)}')
            b.append(f'<text x="164" y="{y}" font-family="{SANS}" font-size="16.5" fill="{OR1}">{esc(v)}</text>')
        else:
            b.append(f'<text x="140" y="{y}" font-family="{SANS}" font-size="16.5" fill="{TXT}">{esc(v)}</text>')
    return wrap(W, h, "".join(b), filename)


def stack(items):
    fs, rowh, gap = 14.5, 44, 10
    rows, cur, curw = [], [], 0
    for t in items:
        cw = 24 + len(t) * fs * 0.6 + 14
        if cur and curw + cw > W:
            rows.append((cur, curw - gap)); cur, curw = [], 0
        cur.append((t, cw)); curw += cw + gap
    rows.append((cur, curw - gap))
    b = []
    for ri, (row, total) in enumerate(rows):
        x, y = (W - total) / 2, ri * rowh
        for t, cw in row:
            b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="34" rx="17" fill="{CARD}" stroke="{BORDER}"/>'
                     f'<circle cx="{x+16:.1f}" cy="{y+17}" r="3.5" fill="{OR}"/>'
                     f'<text x="{x+27:.1f}" y="{y+23}" font-family="{SANS}" font-size="{fs}" fill="{TXT}">{esc(t)}</text>')
            x += cw + gap
    return wrap(W, len(rows) * rowh, "".join(b), "stack")


def journey(nodes):
    h = 214
    step = W / len(nodes)
    b = [f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{BORDER}"/><stop offset="1" stop-color="{OR}"/></linearGradient></defs>',
         f'<line x1="30" y1="68" x2="{W-30}" y2="68" stroke="url(#g)" stroke-width="2"/>']
    for i, (date, title, sub) in enumerate(nodes):
        cx = step * i + step / 2
        last = i == len(nodes) - 1
        b.append(f'<text x="{cx}" y="42" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{OR if last else OR1}">{esc(date)}</text>')
        if last:
            b.append(f'<circle cx="{cx}" cy="68" r="8" fill="{OR}"/>{pulse(cx, 68, 8, 20)}')
        else:
            b.append(f'<circle cx="{cx}" cy="68" r="7" fill="{BG}" stroke="{OR}" stroke-width="2"/>')
        y = 108
        for t in title:
            b.append(f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="700" fill="{TXT}">{esc(t)}</text>')
            y += 22
        y += 2
        for t in sub:
            b.append(f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{MUTED}">{esc(t)}</text>')
            y += 19
    return wrap(W, h, "".join(b), "journey")


def button(label):
    w, h = 150, 46
    return wrap(w, h,
                f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="{CARD}" stroke="{OR}" stroke-width="1.5"/>'
                f'<text x="{w/2-8:.0f}" y="30" text-anchor="middle" font-family="{SANS}" font-size="16.5" font-weight="600" fill="{TXT}">{esc(label)}</text>'
                f'<text x="{w/2 + len(label)*4.8 + 2:.0f}" y="30" font-family="{SANS}" font-size="16.5" fill="{OR}">↗</text>', label)


LANG = {
    "en": dict(
        banner_sub="ML / DATA SCIENCE  ·  MECHATRONICS ENGINEERING",
        sections=[("about", "01", "About"), ("projects", "02", "Projects"), ("journey", "03", "Journey")],
        about_file="martin-javier.profile",
        about_rows=[("studying", "Mechatronics Engineering · UASLP · 2026"),
                    ("working", "Automation Intern · BENEBION"),
                    ("focus", "Machine learning for industrial & signal data"),
                    ("languages", "Spanish (native) · English (B2)"),
                    ("status", "Open to work · available Dec 2026")],
        stats=[("3", "summers teaching", "C++ & ML"), ("2", "projects", "on GitHub"),
               ("B2", "English", "native Spanish"), ("Dec 2026", "available", "to start")],
        cards=[
            ("ai4i", "chart", "Machine Failure Prediction", "AI4I 2020 · Python",
             ["Machine failure risk prediction from sensor data,", "with SHAP interpretability and a FastAPI endpoint."],
             ["Python", "scikit-learn", "SHAP", "FastAPI"],
             [("0.86", "F1"), ("0.95", "Precision"), ("0.78", "Recall")]),
            ("nlp", "text", "Ticket Classifier", "NLP · Python",
             ["Ticket classifier built with classic NLP:", "TF-IDF / embeddings, no LLMs."],
             ["Python", "TF-IDF", "scikit-learn"], None),
            ("raman", "spec", "Raman + 1D CNN", "Deep Learning · Python",
             ["1D CNN that classifies serum Raman spectra", "for renal pathologies."], ["Python", "1D CNN"], None),
            ("pv", "sun", "PV Fault Detection", "I-V curves · MATLAB",
             ["Fault detection in photovoltaic systems", "from I-V curve analysis."], ["MATLAB", "I-V curves"], None),
            ("rastro", "search", "Rastro", "Hackathon · Python",
             ["Synthetic-identity fraud detection,", "Crevolution Hackathon 2026 · Team Redhack."], ["Python", "Fraud detection"], None),
            ("plc", "gear", "PLC Production Line", "Automation · CODESYS",
             ["Automated production line controlled with", "CODESYS on a Raspberry Pi."], ["CODESYS", "Raspberry Pi"], None),
        ],
        stack=["Python", "Pandas", "NumPy", "scikit-learn", "SHAP", "FastAPI", "TF-IDF", "Git"],
        journey=[("2023–2025", ["Instructor"], ["C++ & ML", "UASLP"]),
                 ("May 2026", ["Automation", "Intern"], ["BENEBION", "PLC & SQL"]),
                 ("2026", ["Hackathon"], ["Rastro", "Team Redhack"]),
                 ("2026", ["Graduating"], ["Mechatronics Eng.", "UASLP"]),
                 ("Dec 2026", ["Available"], ["Jr ML /", "Data Science"])],
        buttons=("LinkedIn", "Email", "Kaggle"),
    ),
    "es": dict(
        banner_sub="ML / CIENCIA DE DATOS  ·  INGENIERÍA MECATRÓNICA",
        sections=[("about", "01", "Sobre mí"), ("projects", "02", "Proyectos"), ("journey", "03", "Trayectoria")],
        about_file="martin-javier.perfil",
        about_rows=[("estudio", "Ingeniería Mecatrónica · UASLP · 2026"),
                    ("trabajo", "Becario de automatización · BENEBION"),
                    ("enfoque", "ML para datos industriales y de señales"),
                    ("idiomas", "Español (nativo) · Inglés (B2)"),
                    ("estado", "Abierto a chamba · disponible dic 2026")],
        stats=[("3", "veranos enseñando", "C++ y ML"), ("2", "proyectos", "en GitHub"),
               ("B2", "inglés", "español nativo"), ("Dic 2026", "disponible", "para empezar")],
        cards=[
            ("ai4i", "chart", "Predicción de fallas", "AI4I 2020 · Python",
             ["Predicción de riesgo de falla en maquinaria con", "datos de sensores, SHAP y un endpoint con FastAPI."],
             ["Python", "scikit-learn", "SHAP", "FastAPI"],
             [("0.86", "F1"), ("0.95", "Precisión"), ("0.78", "Recall")]),
            ("nlp", "text", "Clasificador de tickets", "NLP · Python",
             ["Clasificador de tickets con NLP clásico:", "TF-IDF / embeddings, sin LLMs."],
             ["Python", "TF-IDF", "scikit-learn"], None),
            ("raman", "spec", "Raman + CNN 1D", "Deep Learning · Python",
             ["CNN 1D que clasifica espectros Raman de", "suero para patologías renales."], ["Python", "CNN 1D"], None),
            ("pv", "sun", "Detección de fallas FV", "Curvas I-V · MATLAB",
             ["Detección de fallas en sistemas fotovoltaicos", "a partir de curvas I-V."], ["MATLAB", "Curvas I-V"], None),
            ("rastro", "search", "Rastro", "Hackathon · Python",
             ["Detección de fraude por identidad sintética,", "Crevolution Hackathon 2026 · Equipo Redhack."], ["Python", "Detección de fraude"], None),
            ("plc", "gear", "Línea de producción con PLC", "Automatización · CODESYS",
             ["Línea de producción automatizada con", "CODESYS sobre una Raspberry Pi."], ["CODESYS", "Raspberry Pi"], None),
        ],
        stack=["Python", "Pandas", "NumPy", "scikit-learn", "SHAP", "FastAPI", "TF-IDF", "Git"],
        journey=[("2023–2025", ["Instructor"], ["C++ y ML", "UASLP"]),
                 ("Mayo 2026", ["Becario de", "automatización"], ["BENEBION", "PLC y SQL"]),
                 ("2026", ["Hackathon"], ["Rastro", "Equipo Redhack"]),
                 ("2026", ["Egreso"], ["Ing. Mecatrónica", "UASLP"]),
                 ("Dic 2026", ["Disponible"], ["Jr ML /", "Data Science"])],
        buttons=("LinkedIn", "Correo", "Kaggle"),
    ),
}

# ---- QUÉ SE MUESTRA ----
# Para sumar proyectos: añade su slug a KEEP_CARDS (ai4i, nlp, raman, pv, rastro, plc).
# Para la línea de tiempo: índices de KEEP_JOURNEY (0 instructor, 1 intern, 2 hackathon, 3 egreso, 4 disponible).
KEEP_CARDS = ("ai4i", "nlp")
KEEP_JOURNEY = (0, 1, 4)

for _d in LANG.values():
    _d["cards"] = [c for c in _d["cards"] if c[0] in KEEP_CARDS]
    _d["journey"] = [n for i, n in enumerate(_d["journey"]) if i in KEEP_JOURNEY]
    big, l1, l2 = _d["stats"][1]
    _d["stats"][1] = (str(len(_d["cards"])), l1, l2)

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for lang, d in LANG.items():
        out = os.path.join(here, "assets", lang)
        for slug, num, title in d["sections"]:
            save(f"{out}/section-{slug}.svg", section(num, title))
        save(f"{out}/about.svg", about(d["about_file"], d["about_rows"]))
        save(f"{out}/stats.svg", stats(d["stats"]))
        for slug, icon, title, sub, desc, tags, metrics in d["cards"]:
            save(f"{out}/card-{slug}.svg", card(icon, title, sub, desc, tags, metrics))
        save(f"{out}/stack.svg", stack(d["stack"]))
        save(f"{out}/journey.svg", journey(d["journey"]))
        for name, label in zip(("linkedin", "email", "kaggle"), d["buttons"]):
            save(f"{out}/btn-{name}.svg", button(label))
        banner_name = "banner.svg" if lang == "en" else "banner.es.svg"
        subprocess.run([sys.executable, os.path.join(here, "make_banner.py"), NAME, d["banner_sub"],
                        os.path.join(here, "assets", banner_name)], check=True)
    print("assets generados en ./assets")
