"""Genera la ilustración del mapa de los mockups de la landing (`landing/index.html`).

Escribe el SVG dentro del `<template id="map-art">` de index.html (entre los marcadores
`<!--MAP-ART:START-->` y `<!--MAP-ART:END-->`). Es un parcelario inventado (no una zona real) con
los mismos colores que pinta el mapa de la app (`src/components/leaflet-html.ts`): satélite,
cartografía tipo IGN, capa Catastro naranja con lindes negras, finca guardada en verde y parcela
seleccionada.

Uso: python landing/tools/build-map-art.py
"""
import io
import random
import re
from pathlib import Path

W, H = 360, 600
COLS, ROWS = 5, 8
random.seed(7)

# Rejilla de vértices compartidos con un poco de desorden: las parcelas encajan sin huecos.
xs = [0, 64, 142, 214, 290, W]
ys = [0, 70, 138, 214, 280, 352, 428, 506, H]
pts = [
    [
        (
            x + (0 if x in (0, W) else random.uniform(-14, 14)),
            y + (0 if y in (0, H) else random.uniform(-12, 12)),
        )
        for x in xs
    ]
    for y in ys
]


def cell(c, r):
    p = [pts[r][c], pts[r][c + 1], pts[r + 1][c + 1], pts[r + 1][c]]
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in p)


def centroid(c, r):
    p = [pts[r][c], pts[r][c + 1], pts[r + 1][c + 1], pts[r + 1][c]]
    return sum(x for x, _ in p) / 4, sum(y for _, y in p) / 4


SAT = ['#2c4428', '#35502d', '#4b5a30', '#5f5f36', '#6e6640', '#3e5631', '#7a6d48', '#4f6a35']
IGN = ['#f3f0e4', '#eef0df', '#f1ecd9', '#ecefe1']
SAVED = [(2, 3), (3, 1)]
# Surcos de labranza: una trama por orientación, para que cada parcela tenga la suya.
FURROW_ANGLES = [-35, -10, 15, 40, 70]
SELECTED = (1, 5)

sat, ign, cad = [], [], []
for r in range(ROWS):
    for c in range(COLS):
        poly = cell(c, r)
        color = random.choice(SAT)
        furrows = random.randrange(len(FURROW_ANGLES))
        sat.append(
            f'<polygon points="{poly}" fill="{color}"/>'
            f'<polygon points="{poly}" fill="url(#furrows{furrows})" opacity=".3"/>'
        )
        ign.append(f'<polygon points="{poly}" fill="{random.choice(IGN)}"/>')
        cad.append(f'<polygon points="{poly}"/>')

furrow_defs = ''.join(
    f'<pattern id="furrows{i}" width="7" height="7" patternUnits="userSpaceOnUse" '
    f'patternTransform="rotate({a})"><rect width="7" height="2" fill="#000" opacity=".22"/></pattern>'
    for i, a in enumerate(FURROW_ANGLES)
)
saved = ''.join(f'<polygon class="m-finca" points="{cell(c, r)}"/>' for c, r in SAVED)
sx, sy = centroid(*SELECTED)
selected = f'<polygon class="m-sel" points="{cell(*SELECTED)}"/>'

svg = f'''<svg class="map-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
  <defs>
    {furrow_defs}
  </defs>
  <g class="m-sat"><rect width="{W}" height="{H}" fill="#24371f"/>{''.join(sat)}</g>
  <g class="m-ign"><rect width="{W}" height="{H}" fill="#f6f3e8"/>{''.join(ign)}
    <path d="M-10 470 C 60 430, 120 470, 190 420 S 300 380, 370 400" fill="none" stroke="#9cc3e6" stroke-width="5"/>
  </g>
  <g class="m-roads">
    <path class="m-road-casing" d="M-10 120 C 80 150, 150 110, 230 160 S 330 250, 370 230"/>
    <path class="m-road" d="M-10 120 C 80 150, 150 110, 230 160 S 330 250, 370 230"/>
    <path class="m-track" d="M120 -10 C 140 120, 100 260, 170 380 S 210 520, 200 610"/>
  </g>
  <g class="m-cad">{''.join(cad)}</g>
  <g class="m-saved">{saved}</g>
  <g class="m-selected">{selected}
    <circle class="m-tap" cx="{sx:.0f}" cy="{sy:.0f}" r="16"/>
  </g>
  <g class="m-labels">
    <rect x="252" y="196" width="46" height="16" rx="3" fill="#2f9e44"/>
    <text x="275" y="208" text-anchor="middle" class="m-shield">BU-400</text>
    <text x="40" y="104" class="m-label" transform="rotate(12 40 104)">Camino Real</text>
    <text x="150" y="300" class="m-label" transform="rotate(-70 150 300)">Camino del Barranco</text>
    <text x="56" y="458" class="m-label m-label-water">Arroyo</text>
  </g>
  <g class="m-user"><circle cx="300" cy="470" r="14" class="m-user-halo"/><circle cx="300" cy="470" r="6" class="m-user-dot"/></g>
</svg>'''

index = Path(__file__).resolve().parent.parent / 'index.html'
html = index.read_text(encoding='utf-8')
html = re.sub(
    r'<!--MAP-ART:START-->.*?<!--MAP-ART:END-->',
    lambda _: '<!--MAP-ART:START-->' + svg + '<!--MAP-ART:END-->',
    html,
    flags=re.S,
)
io.open(index, 'w', encoding='utf-8', newline='\n').write(html)
print(f'map art: {len(svg)} chars')
