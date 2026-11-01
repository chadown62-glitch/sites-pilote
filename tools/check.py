#!/usr/bin/env python3
"""Contrôles statiques : liens internes, ancres, ressources externes, secrets, bannière, titres."""
import pathlib, re, sys
from html.parser import HTMLParser
ROOT = pathlib.Path(__file__).resolve().parent.parent
errs = []
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.ids=set(); s.h1=0; s.imgnoalt=0; s.ext=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t=='h1': s.h1+=1
        if t=='img' and 'alt' not in a: s.imgnoalt+=1
        for k in ('href','src','action'):
            if k in a and a[k]:
                v=a[k]
                (s.ext if re.match(r'(https?:)?//',v) else s.links).append((t,k,v))
pages = sorted(ROOT.glob('*.html'))
data = {}
for f in pages:
    txt=f.read_text(encoding='utf-8'); p=P(); p.feed(txt); data[f.name]=p
    if 'Démonstration — entreprise fictive' not in txt: errs.append(f'{f.name}: bannière absente')
    if p.h1!=1: errs.append(f'{f.name}: {p.h1} h1')
    if p.imgnoalt: errs.append(f'{f.name}: img sans alt')
    if p.ext: errs.append(f'{f.name}: ressource/lien externe {p.ext}')
for n,p in data.items():
    for t,k,v in p.links:
        if v.startswith('mailto:') or v.startswith('tel:'): errs.append(f'{n}: {v}'); continue
        path,_,frag=v.partition('#')
        tgt = n if not path else path
        if not (ROOT/tgt).exists(): errs.append(f'{n}: lien cassé {v}'); continue
        if frag and tgt.endswith('.html') and frag not in data[tgt].ids: errs.append(f'{n}: ancre absente {v}')
pat = re.compile(r'(api[_-]?key|secret|token|passwd|password|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,})',re.I)
for f in ROOT.rglob('*'):
    if f.is_file() and '.git' not in f.parts and f.suffix in ('.html','.css','.js','.py','.md'):
        for i,l in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
            if pat.search(l) and f.name not in ('check.py',): errs.append(f'{f.relative_to(ROOT)}:{i}: motif sensible possible')
print(f'{len(pages)} pages analysées')
print('\n'.join(errs) if errs else 'OK : aucune anomalie statique')
sys.exit(1 if errs else 0)
