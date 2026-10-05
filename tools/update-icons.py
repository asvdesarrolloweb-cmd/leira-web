"""Actualiza la lista de iconos de Material Symbols que descarga `landing/index.html`.

Google Fonts solo sirve los iconos pedidos en `icon_names=` (ordenados alfabéticamente), así la
fuente pesa unos pocos KB en vez de cientos. Este script recoge todos los nombres usados en
`<span class="ms ...">nombre</span>` y reescribe ese parámetro.

Uso: python landing/tools/update-icons.py
"""
import io
import re
from pathlib import Path

index = Path(__file__).resolve().parent.parent / 'index.html'
html = index.read_text(encoding='utf-8')
names = set(re.findall(r'class="[^"]*\bms\b[^"]*"[^>]*>([a-z0-9_]+)<', html))
names |= {'close'}  # el menú móvil cambia 'menu' por 'close' desde main.js
icons = ','.join(sorted(names))
html, n = re.subn(r'icon_names=[a-z0-9_,]+', 'icon_names=' + icons, html)
assert n == 1, 'no se encontró el parámetro icon_names'
io.open(index, 'w', encoding='utf-8', newline='\n').write(html)
print(f'{len(names)} iconos: {icons}')
