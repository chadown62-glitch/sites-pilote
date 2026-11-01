"""Scénarios synthétiques, sans accès aux comptes ni action externe."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from check import SITE_FILES
from commercial_rules import eligible_draft
from package_demo import package
from preflight import blockers, REQUIRED_GATES

class HistoryRegression(unittest.TestCase):
    def setUp(self):
        self.prospect = dict(country='FR', professional_email_public=True, research_complete=True,
            b2b_relevant=True, web_status='none_found_crosschecked', refused=False,
            unsubscribed=False, bounced=False, already_drafted_or_contacted=False,
            has_reply=False, first_sent_confirmed=False, first_sent_at=None)
        self.context = dict(gmail_checked=True, suppression_checked=True, unsent_initial_drafts=9)
        self.now = datetime(2026, 11, 1, 12, tzinfo=timezone.utc)
    def test_initial_rejects_conflicting_sent_history(self):
        self.prospect.update(first_sent_confirmed=True, first_sent_at='2026-10-01T12:00:00Z')
        self.assertTrue(eligible_draft(self.prospect, self.context, 'initial', self.now))
    def test_initial_rejects_reply_even_if_duplicate_flag_is_false(self):
        self.prospect['has_reply'] = True
        self.assertTrue(eligible_draft(self.prospect, self.context, 'initial', self.now))
    def test_initial_rejects_unknown_sent_history(self):
        self.prospect.pop('first_sent_confirmed')
        self.assertTrue(eligible_draft(self.prospect, self.context, 'initial', self.now))
    def test_actual_168_hours_required_across_spring_clock_change(self):
        self.prospect.update(first_sent_confirmed=True, first_sent_at='2026-03-25T12:00:00+01:00',
                             followup_draft_or_sent=False)
        now = datetime(2026, 4, 1, 12, tzinfo=ZoneInfo('Europe/Paris'))
        self.assertTrue(eligible_draft(self.prospect, self.context, 'followup', now))
        self.assertEqual(eligible_draft(self.prospect, self.context, 'followup', now.replace(hour=13)), [])

class ManualPaymentConfiguration(unittest.TestCase):
    def config(self):
        return {'phase': 'preparation', 'payment_mode': 'manual',
                'gates': {key: {'status': 'verified', 'evidence': 'synthetic-test'}
                          for key in REQUIRED_GATES}}
    def test_manual_does_not_require_automatic_adapter(self):
        cfg = self.config()
        cfg['gates']['authenticated_manual_payment_procedure'] = {'status': 'verified', 'evidence': 'synthetic-test'}
        cfg['gates']['authenticated_payment_adapter'] = {'status': 'blocked', 'evidence': None}
        reasons = blockers(cfg)
        self.assertNotIn('authenticated_payment_adapter', reasons)
        self.assertTrue(reasons)  # aucune activation réelle par un fichier
    def test_manual_requires_its_own_verified_procedure(self):
        cfg = self.config()
        self.assertIn('authenticated_manual_payment_procedure', blockers(cfg))
    def test_malformed_configuration_stays_blocked_without_crash(self):
        for cfg in (None, [], {'gates': None}, {'gates': []},
                    {'gates': {'adult_seller_authorized': True}, 'payment_mode': []}):
            with self.subTest(config=cfg):
                self.assertTrue(blockers(cfg))

class StaticBoundaryRegression(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in SITE_FILES:
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, p)
    def tearDown(self): self.tmp.cleanup()
    def inject(self, name, before, content):
        p = self.root / name
        p.write_text(p.read_text().replace(before, content + before))
    def test_inline_script_cannot_hide_network_operation(self):
        self.inject('index.html', '</head>', '<script>fetch("https://outside.invalid")</script>')
        with self.assertRaises(ValueError): package(self.root)
    def test_embedded_styles_cannot_hide_import(self):
        self.inject('index.html', '</head>', '<style>@import "https://outside.invalid/a.css";</style>')
        with self.assertRaises(ValueError): package(self.root)
    def test_meta_refresh_cannot_redirect(self):
        self.inject('index.html', '</head>', '<meta http-equiv="refresh" content="0;url=https://outside.invalid">')
        with self.assertRaises(ValueError): package(self.root)
    def test_extra_enabled_form_is_rejected(self):
        self.inject('contact.html', '</main>', '<form action="#"><input name="data"><button>Go</button></form>')
        with self.assertRaises(ValueError): package(self.root)
    def test_enabled_field_in_first_disabled_fieldset_legend_is_rejected(self):
        self.inject('contact.html', '<label for="nom">', '<legend><input name="enabled"></legend>')
        with self.assertRaises(ValueError): package(self.root)
    def test_link_to_internal_document_is_rejected(self):
        (self.root / 'notes.txt').write_text('synthetic internal note')
        self.inject('index.html', '</main>', '<a href="notes.txt">Note</a>')
        with self.assertRaises(ValueError): package(self.root)

if __name__ == '__main__': unittest.main()
