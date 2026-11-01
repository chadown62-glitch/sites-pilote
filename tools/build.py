#!/usr/bin/env python3
"""Génère les pages HTML statiques à partir de gabarits simples (aucune dépendance).
Usage : python3 tools/build.py   — les .html à la racine sont les fichiers servis."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
NAV = [("index.html","Accueil"),("entreprise.html","Entreprise"),("prestations.html","Prestations"),
       ("peinture.html","Peinture"),("renovation-interieure.html","Rénovation intérieure"),
       ("realisations.html","Réalisations"),("contact.html","Contact")]

def page(fname, title, desc, body, hero=False):
    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="{h}"{cur if h==fname else ""}>{t}</a></li>' for h,t in NAV)
    if hero:
        main = f'<main id="contenu">{body}</main>'
    else:
        main = f'<main id="contenu"><div class="wrap">{body}</div></main>'
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Atelier Démo (entreprise fictive)</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<div class="demo-banner" role="note">Démonstration — entreprise fictive</div>
<header class="site"><div class="wrap">
<a class="brand" href="index.html">Atelier Démo</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
<nav aria-label="Navigation principale"><ul id="menu">{nav}</ul></nav>
</div></header>
{main}
<footer class="site"><div class="wrap">
<p><strong>Démonstration — entreprise fictive.</strong> « Atelier Démo » n'existe pas : aucune adresse, aucun téléphone, aucune offre réelle.</p>
<ul><li><a href="mentions-legales.html">Mentions légales (trame)</a></li><li><a href="confidentialite.html">Confidentialité (trame)</a></li></ul>
</div></footer>
<script src="js/main.js"></script>
</body>
</html>
'''

CTA = '<p><a class="btn" href="contact.html">Page contact (démonstration)</a></p>'
pages = {}

pages["index.html"] = ("Accueil","Atelier Démo, entreprise fictive de rénovation intérieure : site de démonstration.",
 f'''<section class="hero"><div class="wrap">
<h1>Rénovation intérieure : un site vitrine de démonstration</h1>
<p class="lead">Atelier Démo est une entreprise <strong>imaginaire</strong>. Ce site sert uniquement à tester la production d'un site vitrine statique.</p>
{CTA}</div></section>
<div class="wrap content-spaced">
<h2>Ce que présente ce site</h2>
<div class="grid">
<div class="card"><h3>Peinture</h3><p>Exemple de page dédiée à la peinture intérieure.</p><a href="peinture.html">Voir la page</a></div>
<div class="card"><h3>Rénovation intérieure</h3><p>Exemple de page sur la rénovation d'une pièce ou d'un logement.</p><a href="renovation-interieure.html">Voir la page</a></div>
<div class="card"><h3>Réalisations</h3><p>Exemples illustratifs, tous fictifs.</p><a href="realisations.html">Voir la page</a></div>
</div>
<div class="notice">Tous les textes sont rédigés pour la démonstration. Aucun avis client, aucune certification, aucun chiffre réel n'est présenté.</div>
</div>''', True)

pages["entreprise.html"] = ("L'entreprise","Présentation fictive d'Atelier Démo.",
 '''<h1>L'entreprise</h1>
<p class="lead">Atelier Démo est une société fictive créée pour ce pilote.</p>
<h2>Notre approche (exemple)</h2>
<p>Texte illustratif : écouter le besoin, proposer un devis clair, organiser le chantier, remettre les lieux propres. Ces engagements sont des exemples de contenu et ne décrivent aucune entreprise réelle.</p>
<h2>Valeurs (exemple)</h2>
<ul><li>Clarté du devis</li><li>Respect du planning annoncé</li><li>Soin des finitions</li></ul>
<div class="notice">Aucune identité juridique, aucun numéro d'immatriculation, aucune certification n'est affiché : ils n'existent pas.</div>''')

pages["prestations.html"] = ("Prestations","Exemples de prestations d'une entreprise fictive de rénovation.",
 '''<h1>Prestations</h1>
<p class="lead">Liste d'exemples de services pour un site vitrine de rénovation.</p>
<div class="grid">
<div class="card"><h3>Peinture</h3><p>Murs, plafonds, boiseries.</p><a href="peinture.html">Détails</a></div>
<div class="card"><h3>Rénovation intérieure</h3><p>Cloisons, sols, revêtements, coordination.</p><a href="renovation-interieure.html">Détails</a></div>
<div class="card"><h3>Conseil (exemple)</h3><p>Aide au choix de teintes et de matériaux.</p></div>
</div>
<div class="notice">Aucun tarif n'est indiqué : l'entreprise est fictive et ne propose aucune prestation.</div>''')

pages["peinture.html"] = ("Peinture","Page d'exemple sur la peinture intérieure.",
 f'''<h1>Peinture intérieure</h1>
<p class="lead">Contenu d'exemple pour une page de service.</p>
<h2>Étapes typiques d'un chantier</h2>
<ol><li>Protection du mobilier et des sols</li><li>Préparation des supports (rebouchage, ponçage)</li><li>Application de la sous-couche</li><li>Finitions et nettoyage</li></ol>
<h2>Questions fréquentes (exemple)</h2>
<details><summary>Combien de temps dure un chantier ?</summary><p>Cela dépend de la surface. Réponse illustrative, sans valeur d'engagement.</p></details>
<details><summary>Fournissez-vous la peinture ?</summary><p>Exemple de question : à définir pour une vraie entreprise.</p></details>
{CTA}''')

pages["renovation-interieure.html"] = ("Rénovation intérieure","Page d'exemple sur la rénovation intérieure.",
 f'''<h1>Rénovation intérieure</h1>
<p class="lead">Contenu d'exemple pour une page de service.</p>
<h2>Types de travaux (exemples)</h2>
<ul><li>Pose de revêtements de sol</li><li>Création ou modification de cloisons</li><li>Rénovation de pièces d'eau</li><li>Coordination de plusieurs corps de métier</li></ul>
<div class="notice">Certains travaux exigent des qualifications ou assurances spécifiques : à documenter pour toute vraie entreprise.</div>
{CTA}''')

pages["realisations.html"] = ("Réalisations","Exemples illustratifs fictifs de réalisations.",
 '''<h1>Réalisations</h1>
<div class="notice"><strong>Réalisations fictives.</strong> Les cartes ci-dessous sont des emplacements illustratifs : aucune photo, aucun chantier ni client réel.</div>
<div class="grid">
<div class="card"><div class="ph" role="img" aria-label="Emplacement photo fictif">Emplacement photo (fictif)</div><h3>Salon — exemple</h3><p>Description inventée pour la démonstration.</p></div>
<div class="card"><div class="ph" role="img" aria-label="Emplacement photo fictif">Emplacement photo (fictif)</div><h3>Cuisine — exemple</h3><p>Description inventée pour la démonstration.</p></div>
<div class="card"><div class="ph" role="img" aria-label="Emplacement photo fictif">Emplacement photo (fictif)</div><h3>Chambre — exemple</h3><p>Description inventée pour la démonstration.</p></div>
</div>''')

pages["contact.html"] = ("Contact","Page contact de démonstration : formulaire désactivé.",
 '''<h1>Contact</h1>
<div class="notice todo"><strong>Formulaire de démonstration désactivé.</strong> Rien n'est envoyé, enregistré ni traité. Aucune adresse ni aucun téléphone n'est publié car l'entreprise est fictive.</div>
<form id="demo-form" action="#" aria-describedby="demo-info">
<p id="demo-info">Les champs sont désactivés : ce formulaire illustre seulement la mise en page.</p>
<fieldset disabled class="demo-fields">
<label for="nom">Nom</label><input id="nom" type="text" autocomplete="off">
<label for="email">Adresse e-mail</label><input id="email" type="email" autocomplete="off">
<label for="msg">Message</label><textarea id="msg" rows="5"></textarea>
<p class="form-actions"><button class="btn" type="submit" disabled>Envoi indisponible (démonstration)</button></p>
</fieldset></form>''')

pages["mentions-legales.html"] = ("Mentions légales (trame)","Trame de mentions légales à compléter et vérifier avant publication.",
 '''<h1>Mentions légales — trame</h1>
<div class="notice todo"><strong>À compléter et vérifier avant publication.</strong> Cette trame n'a aucune valeur juridique et ne désigne aucune personne ni société réelle.</div>
<h2>Éditeur du site</h2><p>[Dénomination, forme juridique, adresse, immatriculation : à compléter]</p>
<h2>Directeur de la publication</h2><p>[À compléter]</p>
<h2>Hébergeur</h2><p>[Nom et coordonnées de l'hébergeur : à compléter]</p>
<h2>Contact</h2><p>[Moyen de contact : à compléter]</p>
<h2>Propriété intellectuelle</h2><p>[À compléter]</p>
<h2>Autres mentions éventuelles</h2><p>[Assurances, qualifications, médiation… : à déterminer avec un professionnel du droit]</p>''')

pages["confidentialite.html"] = ("Confidentialité (trame)","Trame de politique de confidentialité à compléter et vérifier avant publication.",
 '''<h1>Politique de confidentialité — trame</h1>
<div class="notice todo"><strong>À compléter et vérifier avant publication.</strong> Cette trame n'a aucune valeur juridique.</div>
<h2>Situation de ce site de démonstration</h2>
<p>Le code de cette démonstration ne charge aucun contenu externe, ne met en place aucun traceur ni cookie et son formulaire est désactivé. En consultation locale, ce formulaire ne transmet rien. Une consultation via un serveur peut générer des journaux techniques : leur contenu, leurs destinataires et leur durée de conservation devront être vérifiés selon l’hébergement retenu.</p>
<h2>Si un traitement de données était ajouté</h2>
<p>[Responsable du traitement, finalités, base légale, durées de conservation, destinataires, droits des personnes, contact : à compléter]</p>''')

for f,(t,d,b,*h) in pages.items():
    (ROOT/f).write_text(page(f,t,d,b,bool(h and h[0])), encoding="utf-8")
print(len(pages),"pages générées")

