#!/usr/bin/env python3
"""
Add a site header to all html files under games/ that don't already contain one.
Run from repo root: python3 scripts/add_header.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAMES = ROOT / 'games'

header_html = '''
<header class="site-header" style="display:flex;align-items:center;gap:12px;padding:12px 16px;background:linear-gradient(90deg,#0b6fbf,#0b88e0);color:#fff">
    <div style="display:flex;align-items:center;gap:10px">
    <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="width:36px;height:36px"><rect rx="8" width="64" height="64" fill="#fff"/><path d="M14 32c0-8 6-12 14-12s14 4 14 12-6 12-14 12S14 40 14 32z" fill="#0b6fbf"/><circle cx="24" cy="30" r="3" fill="#fff"/><circle cx="34" cy="30" r="3" fill="#fff"/><rect x="20" y="36" width="4" height="4" rx="1" fill="#fff"/></svg>
    <div style="font-weight:700">JesusOnTop Games</div>
  </div>
  <nav style="margin-left:auto;display:flex;gap:8px;align-items:center">
    <a href="../index.html" style="background:rgba(255,255,255,0.95);color:#08324a;padding:8px 10px;border-radius:8px;text-decoration:none;font-weight:700">Home</a>
    <a href="index.html" style="background:rgba(255,255,255,0.95);color:#08324a;padding:8px 10px;border-radius:8px;text-decoration:none;font-weight:700">Games Hub</a>
  </nav>
</header>
'''

count=0
skipped=0
for p in sorted(GAMES.glob('*.html')):
    try:
        txt = p.read_text(encoding='utf-8')
    except Exception:
        print(f"skip (read error): {p}")
        continue
    # skip files that already include site-header
    if 'class="site-header"' in txt or 'class=\'site-header\'' in txt:
        skipped += 1
        continue
    m = re.search(r'<body[^>]*>', txt, flags=re.IGNORECASE)
    if not m:
        print(f"no <body> tag found, skipping: {p}")
        skipped += 1
        continue
    new_txt = txt[:m.end()] + '\n' + header_html + txt[m.end():]
    p.write_text(new_txt, encoding='utf-8')
    count += 1

print(f"Inserted header into {count} files; skipped {skipped} files.")
