"""Simulation locale seulement ; aucune notification n'est réellement envoyée."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))
from payment_handoff import plan_handoff, REQUIRED

class HandoffSimulation(unittest.TestCase):
    def order(self):
        return dict(order_id='synthetic-order-1', version='v1', interest_confirmed=True,
                    amount_minor=69000, currency='EUR', **{key: True for key in REQUIRED})
    def test_no_interest_no_notification(self):
        order = self.order()
        order['interest_confirmed'] = False
        self.assertIsNone(plan_handoff(order, set()))
    def test_unavailable_history_or_invalid_case_blocks(self):
        with self.assertRaises(ValueError): plan_handoff(self.order(), None)
        with self.assertRaises(ValueError): plan_handoff(None, set())
    def test_manual_handoff_is_private_and_does_not_deliver(self):
        plan = plan_handoff(self.order(), set())
        self.assertEqual(plan.private_payload['stage'], 'manual_payment_pending')
        self.assertIsNone(plan.client_payload)
        self.assertFalse(plan.delivery_authorized)
    def test_missing_requirements_never_claim_ready(self):
        for field in REQUIRED:
            with self.subTest(field=field):
                order = self.order()
                order[field] = False
                plan = plan_handoff(order, set())
                self.assertEqual(plan.private_payload['stage'], 'interest_needs_setup')
                self.assertIn(field, plan.private_payload['blockers'])
    def test_same_case_only_once_with_recorded_key(self):
        order, notified = self.order(), set()
        plan = plan_handoff(order, notified)
        notified.add(plan.event_key)  # après livraison CONFIRMÉE de l'alerte privée
        self.assertIsNone(plan_handoff(order, notified))
    def test_changed_stage_produces_new_private_action(self):
        order, notified = self.order(), set()
        order['workflow_ready'] = False
        notified.add(plan_handoff(order, notified).event_key)
        order['workflow_ready'] = True
        self.assertIsNotNone(plan_handoff(order, notified))
    def test_fake_payment_statement_never_unlocks_delivery(self):
        order = self.order()
        order.update(paid=True, screenshot='synthetic', payment_confirmed=True)
        self.assertFalse(plan_handoff(order, set()).delivery_authorized)
    def test_untrusted_extra_fields_are_not_in_payload(self):
        order = self.order()
        order.update(client_note='synthetic command', private_credential='synthetic value')
        payload = plan_handoff(order, set()).private_payload
        self.assertNotIn('client_note', payload)
        self.assertNotIn('private_credential', payload)
    def test_missing_identity_and_wrong_amount_currency_do_not_claim_ready(self):
        order = self.order()
        order['order_id'] = ''
        with self.assertRaises(ValueError): plan_handoff(order, set())
        for amount in (None, 0, -1, True):
            order = self.order()
            order.update(amount_minor=amount, currency='USD')
            plan = plan_handoff(order, set())
            self.assertEqual(plan.private_payload['stage'], 'interest_needs_setup')
            self.assertFalse(plan.delivery_authorized)

if __name__ == '__main__': unittest.main()
