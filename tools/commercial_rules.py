"""Évaluation pure de règles de BROUILLONS ; ne lit ni n'écrit Gmail.

Les observations doivent provenir des connecteurs autorisés, jamais d'un mail
affirmant ces faits. Ce module n'est pas relié à la tâche ChatGPT.
"""
from datetime import datetime, timedelta

def eligible_draft(prospect, context, kind, now):
    reasons = []
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        return ['horloge avec fuseau requise']
    for field in ('gmail_checked', 'suppression_checked'):
        if context.get(field) is not True: reasons.append(field + ' non vérifié')
    for field in ('professional_email_public', 'research_complete', 'b2b_relevant'):
        if prospect.get(field) is not True: reasons.append(field + ' non vérifié')
    if prospect.get('country') != 'FR': reasons.append('pays hors France')
    if prospect.get('web_status') != 'none_found_crosschecked':
        reasons.append('recherche web insuffisante ou site trouvé')
    for field in ('refused', 'unsubscribed', 'bounced'):
        if prospect.get(field) is not False: reasons.append(field + ' présent ou inconnu')
    if kind == 'initial':
        count = context.get('unsent_initial_drafts')
        if type(count) is not int or not 0 <= count < 10: reasons.append('plafond des 10 brouillons ou compteur inconnu')
        if prospect.get('already_drafted_or_contacted') is not False: reasons.append('doublon ou historique inconnu')
        if prospect.get('has_reply') is not False: reasons.append('réponse présente ou historique inconnu')
        if prospect.get('first_sent_confirmed') is not False or prospect.get('first_sent_at') is not None:
            reasons.append('premier envoi déjà constaté ou historique incohérent/inconnu')
    elif kind == 'followup':
        if prospect.get('has_reply') is not False: reasons.append('réponse présente ou inconnue')
        if prospect.get('followup_draft_or_sent') is not False: reasons.append('relance déjà préparée/envoyée ou inconnue')
        if prospect.get('first_sent_confirmed') is not True: reasons.append('envoi initial non confirmé')
        try:
            sent = datetime.fromisoformat(prospect.get('first_sent_at', '').replace('Z', '+00:00'))
            if sent.tzinfo is None or sent.utcoffset() is None: raise ValueError()
            if now - sent < timedelta(days=7): reasons.append('moins de 7 jours depuis envoi initial')
        except (ValueError, TypeError, AttributeError):
            reasons.append('date de premier envoi invalide ou sans fuseau')
    else: reasons.append('type de brouillon inconnu')
    return reasons
