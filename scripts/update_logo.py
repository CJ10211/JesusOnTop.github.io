#!/usr/bin/env python3
"""
Replace the first <svg> inside a header with a cross SVG for all HTML files under games/.
Run from repo root: python3 scripts/update_logo.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAMES = ROOT / 'games'

cross_svg = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="width:36px;height:36px">
  <rect rx="8" width="64" height="64" fill="#fff"/>
  <rect x="28" y="8" width="8" height="48" fill="#0b6fbf"/>
  <rect x="12" y="28" width="40" height="8" fill="#0b6fbf"/>
</svg>'''

count = 0
for p in sorted(GAMES.glob('*.html')):
    txt = p.read_text(encoding='utf-8')
    # find header section
    hmatch = re.search(r'(<header[^>]*class="site-header"[\s\S]*?</header>)', txt, flags=re.IGNORECASE)
    if not hmatch:
        continue
    header_html = hmatch.group(1)
    # find first svg in header
    sv_match = re.search(r'<svg[\s\S]*?</svg>', header_html, flags=re.IGNORECASE)
    if not sv_match:
        continue
    new_header = header_html[:sv_match.start()] + cross_svg + header_html[sv_match.end():]
    new_txt = txt[:hmatch.start(1)] + new_header + txt[hmatch.end(1):]
    p.write_text(new_txt, encoding='utf-8')
    count += 1

print(f"Replaced logo SVG in {count} game files.")
