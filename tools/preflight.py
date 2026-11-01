#!/usr/bin/env python3
"""Lecture seule : aucun connecteur, envoi, paiement, publication ou livraison."""
import json
from pathlib import Path
import sys

REQUIRED_GATES = (
    'adult_seller_authorized', 'declared_activity_checked', 'tax_and_contract_approved',
    'professional_sender_and_privacy_notice', 'private_state_and_suppression_sync',
    'private_payment_handoff_live',
    'isolated_preview_and_delivery',
    'end_to_end_recovery_test', 'adult_operator_accounts_and_quotas',
    'prospect_sources_revalidated_before_send',
)

def blockers(config):
    result = []
    if not isinstance(config, dict):
        return ['configuration invalide', 'aucun adaptateur exécutable de vente/paiement/livraison dans ce pilote']
    if config.get('phase') != 'live': result.append('phase : préparation, actions externes interdites')
    gates = config.get('gates')
    if not isinstance(gates, dict):
        result.append('liste des contrôles absente ou invalide')
        gates = {}
    payment_gates = {'manual': 'authenticated_manual_payment_procedure',
                     'automated': 'authenticated_payment_adapter'}
    mode = config.get('payment_mode')
    payment_gate = payment_gates.get(mode) if isinstance(mode, str) else None
    if payment_gate is None: result.append('mode de paiement manuel/automatisé à définir')
    for key in (*REQUIRED_GATES, *((payment_gate,) if payment_gate else ())):
        gate = gates.get(key, {})
        if not isinstance(gate, dict): gate = {}
        if gate.get('status') != 'verified' or not isinstance(gate.get('evidence'), str) or not gate['evidence'].strip():
            result.append(key)
    # Même un fichier renseigné ne remplace pas des adaptateurs authentifiés/testés.
    result.append('aucun adaptateur exécutable de vente/paiement/livraison dans ce pilote')
    return result

if __name__ == '__main__':
    config = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) == 2 else {}
    result = blockers(config)
    print('PRÉPARATION UNIQUEMENT — bilan de configuration, sans action externe')
    for item in result: print('- BLOQUÉ : ' + item)
    sys.exit(2 if result else 0)
