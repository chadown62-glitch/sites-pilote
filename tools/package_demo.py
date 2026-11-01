#!/usr/bin/env python3
"""Paquet du PILOTE FICTIF uniquement ; ne remet rien à un client, ne publie rien."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile
from check import ROOT, SITE_FILES, check_site

def package(root=ROOT):
    root = Path(root).resolve()
    errors = check_site(root)
    if errors: raise ValueError('Contrôles en échec : ' + '; '.join(errors))
    out = root / 'out'
    if out.is_symlink(): raise ValueError('out ne doit pas être un lien symbolique')
    out.mkdir(exist_ok=True)
    target = out / 'atelier-demo.zip'
    manifest_path = out / 'manifest.json'
    if target.is_symlink() or manifest_path.is_symlink():
        raise ValueError('archive ou manifeste symbolique interdit')
    manifest = {}
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name in SITE_FILES:
            data = (root / name).read_bytes()
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
            manifest[name] = sha256(data).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    return target, manifest

if __name__ == '__main__':
    target, manifest = package()
    print(f'Paquet fictif local : {target.name} ; {len(manifest)} fichiers autorisés')
    print('Non publié ; ne contient ni outil, rapport, dossier client ni configuration interne.')
