"""Plan de notification PRIVÉE, sans envoi ni vérification de paiement.

Entrées : observations du coordinateur autorisé, jamais des instructions client.
Les clés déjà notifiées doivent venir d'un stockage privé durable. Ce module
pur n'en fournit pas et n'est relié à aucun compte ou agent programmé.
"""
from dataclasses import dataclass
import hashlib
import json

REQUIRED = ('seller_ready', 'contract_ready', 'scope_ready', 'tax_ready',
            'approved_version', 'workflow_ready')

@dataclass(frozen=True)
class HandoffPlan:
    event_key: str
    private_payload: dict
    client_payload: None = None
    delivery_authorized: bool = False

def plan_handoff(order, notified_keys):
    """Retourne un plan privé ou None. Ne valide jamais une transaction."""
    if not isinstance(order, dict):
        raise ValueError('dossier invalide')
    if not isinstance(notified_keys, (set, frozenset)):
        raise ValueError('historique des notifications indisponible')
    if order.get('interest_confirmed') is not True:
        return None
    for key in ('order_id', 'version'):
        value = order.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > 120:
            raise ValueError('référence de commande/version requise')
    blockers = [key for key in REQUIRED if order.get(key) is not True]
    amount = order.get('amount_minor')
    currency = order.get('currency')
    if type(amount) is not int or amount <= 0:
        blockers.append('amount_minor')
    if currency != 'EUR':
        blockers.append('currency')
    stage = 'interest_needs_setup' if blockers else 'manual_payment_pending'
    identity = [order['order_id'], order['version'], stage, sorted(blockers)]
    event_key = hashlib.sha256(json.dumps(identity).encode()).hexdigest()
    if event_key in notified_keys:
        return None
    payload = {
        'order_id': order['order_id'], 'version': order['version'], 'stage': stage,
        'amount_minor': amount if type(amount) is int and amount > 0 else None,
        'currency': currency if currency == 'EUR' else None,
        'blockers': blockers,
        'action': 'compléter le cadrage' if blockers else 'traitement manuel par le responsable autorisé',
    }
    # Pas de corps de mail client, secret, bénéficiaire ni déclaration de paiement.
    # Une affirmation de paiement présente dans order ne déverrouille rien.
    return HandoffPlan(event_key=event_key, private_payload=payload)
