"""Essai fictif de reprise : modifier une page sans reconstruire les autres."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from check import SITE_FILES, PAGES, check_site

class RevisionFlow(unittest.TestCase):
    def test_targeted_revision_and_reproducible_build(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in (*SITE_FILES, 'tools/build.py'):
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, p)
            before = {name: (root / name).read_bytes() for name in PAGES}
            subprocess.run([sys.executable, str(root / 'tools/build.py')], check=True, capture_output=True)
            self.assertEqual(before, {name: (root / name).read_bytes() for name in PAGES})
            generator = root / 'tools/build.py'
            text = generator.read_text()
            text = text.replace("<h2>Étapes typiques d'un chantier</h2>",
                                '<h2>Préparation et étapes — modification fictive</h2>')
            self.assertNotEqual(text, generator.read_text())
            generator.write_text(text)
            subprocess.run([sys.executable, str(generator)], check=True, capture_output=True)
            changed = [name for name in PAGES if before[name] != (root / name).read_bytes()]
            self.assertEqual(changed, ['peinture.html'])
            self.assertEqual(check_site(root), [])

if __name__ == '__main__': unittest.main()
