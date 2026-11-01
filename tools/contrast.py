#!/usr/bin/env python3
"""Mesure de paires connues du CSS. Pas un audit visuel global."""
import json
from pathlib import Path
import re

def luminance(color):
    color = color.lstrip('#')
    if len(color) == 3: color = ''.join(c * 2 for c in color)
    rgb = [int(color[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    return sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))

def ratio(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + .05) / (low + .05)

def measure():
    css = (Path(__file__).resolve().parent.parent / 'css/style.css').read_text()
    colors = dict(re.findall(r'--([a-z-]+):\s*(#[0-9a-fA-F]{3,6})\b', css))
    pairs = [('texte', colors['fg'], colors['bg']), ('secondaire', colors['muted'], colors['bg']),
             ('lien', colors['accent'], colors['bg']), ('bouton', colors['accent-fg'], colors['accent']),
             ('bannière', '#3d3000', colors['banner']), ('pied de page', '#eeeeee', '#2b2620'),
             ('lien pied de page', '#ffd9bf', '#2b2620'), ('emplacement photo clair', colors['muted'], '#f1e9dc'),
             ('emplacement photo foncé', colors['muted'], '#e8ddcd')]
    return [{'pair': label, 'ratio': round(ratio(fg, bg), 2), 'normal_text_4_5': ratio(fg, bg) >= 4.5}
            for label, fg, bg in pairs]

if __name__ == '__main__':
    result = measure()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(any(not r['normal_text_4_5'] for r in result))
