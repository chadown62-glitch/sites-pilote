#!/usr/bin/env python3
"""Contrôles limités du pilote, sans réseau. Ne constitue pas un audit exhaustif."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGES = ('index.html', 'entreprise.html', 'prestations.html', 'peinture.html',
         'renovation-interieure.html', 'realisations.html', 'contact.html',
         'mentions-legales.html', 'confidentialite.html')
ASSETS = ('css/style.css', 'js/main.js')
SITE_FILES = PAGES + ASSETS
SECRET_PATTERNS = (
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
    re.compile(r'\bgithub_pat_[A-Za-z0-9_]{40,}\b'),
    re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}\b'),
    re.compile(r"""(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\s*[:=]\s*["'][^"'\s]{16,}["']"""),
)

def possible_secret(text):
    return any(p.search(text) for p in SECRET_PATTERNS)

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.urls, self.ids, self.duplicates, self.errors = [], set(), set(), []
        self.h1, self.main, self.title, self.lang, self.noindex = 0, 0, 0, None, False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.lang = attrs.get('lang')
        if tag == 'h1': self.h1 += 1
        if tag == 'main': self.main += 1
        if tag == 'title': self.title += 1
        if 'id' in attrs:
            if attrs['id'] in self.ids: self.duplicates.add(attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.noindex = 'noindex' in attrs.get('content', '')
        if tag == 'img' and 'alt' not in attrs: self.errors.append('image sans alt')
        if tag in ('iframe', 'object', 'embed', 'base'): self.errors.append('élément exclu du pilote : ' + tag)
        if any(k.lower().startswith('on') for k in attrs): self.errors.append('gestionnaire JS inline')
        if 'style' in attrs: self.errors.append('style inline : utiliser le CSS commun')
        if 'srcset' in attrs: self.errors.append('srcset non pris en charge par ce contrôle')
        for key in ('href', 'src', 'action', 'poster', 'data'):
            if attrs.get(key): self.urls.append(attrs[key])

def check_site(root=ROOT):
    root = Path(root).resolve()
    errors, docs = [], {}
    if {p.name for p in root.glob('*.html')} != set(PAGES):
        errors.append('les 9 pages attendues doivent être présentes, sans page supplémentaire')
    for name in SITE_FILES:
        p = root / name
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):
            errors.append(name + ': fichier absent ou lien symbolique interdit')
            continue
        text = p.read_text(encoding='utf-8')
        if possible_secret(text): errors.append(name + ': motif sensible possible (valeur masquée)')
        if name.endswith('.html'):
            d = docs[name] = Document(text)
            if d.lang != 'fr' or d.h1 != 1 or d.main != 1 or d.title != 1:
                errors.append(name + ': langue/titre/h1/main incorrect')
            if not d.noindex or 'Démonstration — entreprise fictive' not in text:
                errors.append(name + ': signalement fictif/noindex absent')
            errors.extend(name + ': ' + e for e in d.errors)
            if d.duplicates: errors.append(name + ': identifiants dupliqués')
        elif name.endswith('.css'):
            if re.search(r'@import\b', text, re.I): errors.append(name + ': import CSS exclu')
            for url in re.findall(r'url\(\s*[\"\']?([^\s)\"\']+)', text, re.I):
                if urlsplit(url).scheme or url.startswith('//'):
                    errors.append(name + ': URL non locale dans CSS')
        elif re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\b|https?://', text):
            errors.append(name + ': réseau exclu du JavaScript du pilote')
    for name, d in docs.items():
        for url in d.urls:
            u = urlsplit(url)
            if u.scheme or u.netloc or u.query or u.path.startswith('/') or '\\' in u.path:
                errors.append(name + ': URL non locale ou non prise en charge')
                continue
            target = (root / unquote(u.path)).resolve() if u.path else root / name
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(name + ': lien absent ou sortant du dossier')
                continue
            if u.fragment and (target.name not in docs or unquote(u.fragment) not in docs[target.name].ids):
                errors.append(name + ': ancre absente')
    for name in ('mentions-legales.html', 'confidentialite.html'):
        p = root / name
        if p.is_file() and 'À compléter et vérifier avant publication' not in p.read_text():
            errors.append(name + ': avertissement juridique absent')
    contact = root / 'contact.html'
    if contact.is_file():
        text = contact.read_text()
        if '<fieldset disabled' not in text or 'type="submit" disabled' not in text:
            errors.append('contact.html: formulaire de démonstration non désactivé')
    return errors

def check_sources(root=ROOT):
    """Balayage ciblé des fichiers texte ; pas de preuve d'absence de tout secret."""
    errors = []
    for p in Path(root).rglob('*'):
        if any(part in ('.git', 'out', 'node_modules', '.venv', '__pycache__') for part in p.parts):
            continue
        if not p.is_file(): continue
        if p.name == '.env' or p.name.startswith('.env.') or p.suffix in ('.pem', '.key', '.p12'):
            errors.append(str(p.relative_to(root)) + ': fichier privé interdit')
        elif p.suffix in ('.html', '.css', '.js', '.cjs', '.py', '.md', '.json'):
            if possible_secret(p.read_text(encoding='utf-8')):
                errors.append(str(p.relative_to(root)) + ': motif sensible possible (valeur masquée)')
    return errors

if __name__ == '__main__':
    errors = check_site() + check_sources()
    print(f'{len(PAGES)} pages attendues ; contrôles locaux de contenu, liens et motifs sensibles')
    print('\n'.join(errors) if errors else 'OK : aucune anomalie dans le périmètre contrôlé')
    sys.exit(bool(errors))
