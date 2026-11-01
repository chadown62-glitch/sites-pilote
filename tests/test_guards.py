from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from check import SITE_FILES, check_site, possible_secret
from commercial_rules import eligible_draft
from package_demo import package
from preflight import blockers, REQUIRED_GATES

class DraftRules(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 1, 12, tzinfo=timezone.utc)
        self.p = dict(country='FR', professional_email_public=True, research_complete=True,
                      b2b_relevant=True, web_status='none_found_crosschecked', refused=False,
                      unsubscribed=False, bounced=False, already_drafted_or_contacted=False,
                      has_reply=False, followup_draft_or_sent=False, first_sent_confirmed=True,
                      first_sent_at=(self.now - timedelta(days=7)).isoformat())
        self.c = dict(gmail_checked=True, suppression_checked=True, unsent_initial_drafts=9)
    def initial(self):
        # Un premier contact n'a aucun envoi antérieur, contrairement au cas relance.
        prospect = dict(self.p, first_sent_confirmed=False, first_sent_at=None)
        return eligible_draft(prospect, self.c, 'initial', self.now)
    def followup(self): return eligible_draft(self.p, self.c, 'followup', self.now)
    def test_cap_boundary(self):
        self.assertEqual(self.initial(), [])
        for n in (10, 11, -1, None, True):
            self.c['unsent_initial_drafts'] = n
            self.assertTrue(self.initial(), n)
    def test_refusal_and_delivery_error_take_priority(self):
        for f in ('refused', 'unsubscribed', 'bounced'):
            with self.subTest(f=f):
                self.p[f] = True
                self.assertTrue(self.initial())
                self.assertTrue(self.followup())
                self.p[f] = False
    def test_duplicates_and_missing_history_block(self):
        self.p['already_drafted_or_contacted'] = True
        self.assertTrue(self.initial())
        self.p.pop('already_drafted_or_contacted')
        self.assertTrue(self.initial())
    def test_exact_seven_days_and_one_second_before(self):
        self.assertEqual(self.followup(), [])
        self.p['first_sent_at'] = (self.now - timedelta(days=7) + timedelta(seconds=1)).isoformat()
        self.assertTrue(self.followup())
    def test_draft_is_not_sent(self):
        self.p['first_sent_confirmed'] = False
        self.assertTrue(self.followup())
    def test_reply_or_existing_followup_blocks(self):
        for f in ('has_reply', 'followup_draft_or_sent'):
            self.p[f] = True
            self.assertTrue(self.followup())
            self.p[f] = False
    def test_uncertain_research_or_suppression_blocks(self):
        for f in ('gmail_checked', 'suppression_checked'):
            self.c[f] = False
            self.assertTrue(self.initial())
            self.c[f] = True
        for value in ('website_found', 'unknown', None):
            self.p['web_status'] = value
            self.assertTrue(self.initial())
    def test_future_invalid_naive_dates_block(self):
        for value in ((self.now + timedelta(days=1)).isoformat(), 'incorrect', '2026-10-01T12:00:00'):
            self.p['first_sent_at'] = value
            self.assertTrue(self.followup())
        self.assertTrue(eligible_draft(self.p, self.c, 'initial', datetime(2026, 11, 1)))
    def test_same_instant_in_other_timezone(self):
        self.p['first_sent_at'] = '2026-10-25T13:00:00+01:00'
        self.assertEqual(self.followup(), [])
    def test_scope_and_unknown_kind(self):
        self.p['country'] = 'BE'
        self.assertTrue(self.initial())
        self.assertTrue(eligible_draft(self.p, self.c, 'send', self.now))

class PackageGuards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for f in SITE_FILES:
            target = self.root / f
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / f, target)
    def tearDown(self): self.tmp.cleanup()
    def test_package_excludes_private_and_internal_files(self):
        (self.root / 'private').mkdir()
        (self.root / 'private/client.txt').write_text('synthetic only')
        (self.root / 'README.md').write_text('internal')
        first, manifest = package(self.root)
        data = first.read_bytes()
        with zipfile.ZipFile(first) as z:
            self.assertEqual(set(z.namelist()), set(SITE_FILES))
        second, _ = package(self.root)
        self.assertEqual(data, second.read_bytes())
        with zipfile.ZipFile(second) as z:
            restored = self.root / 'restored'
            z.extractall(restored)
        self.assertEqual(check_site(restored), [])
        self.assertEqual(len(manifest), 11)
    def test_secret_marker_blocks_package(self):
        with (self.root / 'js/main.js').open('a') as f:
            f.write('\n/* ' + 'gh' + 'p_' + 'A' * 40 + ' */')
        with self.assertRaises(ValueError): package(self.root)
    def test_documentation_about_secrets_is_not_a_credential(self):
        self.assertFalse(possible_secret('Absence de secrets vérifiée dans le périmètre du contrôle.'))
    def test_symlink_escape_blocks(self):
        p = self.root / 'css/style.css'
        p.unlink()
        p.symlink_to(ROOT / 'css/style.css')
        with self.assertRaises(ValueError): package(self.root)
    def test_injected_external_resource_blocks(self):
        p = self.root / 'index.html'
        p.write_text(p.read_text().replace('</head>', '<script src="//outside.invalid/a.js"></script></head>'))
        with self.assertRaises(ValueError): package(self.root)
    def test_missing_legal_notice_blocks(self):
        p = self.root / 'mentions-legales.html'
        p.write_text(p.read_text().replace('À compléter et vérifier avant publication', ''))
        with self.assertRaises(ValueError): package(self.root)
    def test_configuration_cannot_enable_live_operations(self):
        cfg = {'phase': 'preparation', 'gates': {key: {'status': 'unverified', 'evidence': None} for key in REQUIRED_GATES}}
        self.assertTrue(blockers(cfg))
        cfg['phase'] = 'live'
        for gate in cfg['gates'].values():
            gate.update(status='verified', evidence='synthetic')
        self.assertTrue(blockers(cfg))

if __name__ == '__main__': unittest.main()
