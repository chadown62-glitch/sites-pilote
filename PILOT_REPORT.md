# PILOT_REPORT — Atelier Démo (entreprise fictive)

Date : 2026-11-01. Dépôt initialement vide ; site construit en une passe.

## Fichiers produits
- Pages : `index.html`, `entreprise.html`, `prestations.html`, `peinture.html`, `renovation-interieure.html`, `realisations.html`, `contact.html`, `mentions-legales.html`, `confidentialite.html`
- `css/style.css`, `js/main.js`
- `tools/build.py` (génération des pages), `tools/check.py` (contrôles statiques)
- `README.md`, `PILOT_REPORT.md`

## Choix
HTML/CSS/JS pur, aucune dépendance. Bannière « Démonstration — entreprise fictive » sur chaque page + pied de page. `noindex` posé. Réalisations = emplacements fictifs sans image. Aucun avis, certification, tarif, adresse ou téléphone.

## Contrôles exécutés (constatés)
- `tools/check.py` : 9 pages ; liens internes et ancres valides, 0 ressource externe, bannière et un seul h1 par page, aucun motif de secret → OK.
- Chromium headless (Playwright) sur les 9 pages, viewports 375 px et 1280 px : 0 erreur JS/console, 0 requête réseau externe, 0 débordement horizontal.
- Clavier : lien d'évitement reçoit le premier focus ; menu mobile ouvrable à Entrée, fermable par Échap, `aria-expanded` mis à jour.
- Contact : tous les champs et le bouton sont désactivés ; la soumission est bloquée.

## Contrôles non effectués / impossibles
- Aucun test avec lecteur d'écran réel, ni audit de contraste automatisé (contrastes choisis à la main, non mesurés).
- Pas de test sur Firefox/Safari ni sur appareils physiques.
- Aucune validation HTML par le validateur W3C (hors ligne).
- Pas de revue juridique : aucune conformité n'est affirmée.

## Problèmes restants
- Les `.html` générés sont versionnés ; modifier à la main puis régénérer écraserait les changements.
- Pas d'images ni de favicon (volontaire : aucun contenu copié).
- Le menu mobile repose sur JS ; sans JS, la navigation reste visible en liste normale.

## Conditions avant une publication réelle
1. Remplacer le contenu fictif par celui d'une vraie entreprise, avec son accord et des éléments vérifiables (aucun avis/certification inventé).
2. Faire compléter et valider les mentions légales et la politique de confidentialité par un professionnel compétent.
3. Décider du traitement du formulaire (hébergeur, base légale, information des personnes, sécurité) avant de l'activer.
4. Fournir des images dont les droits sont maîtrisés ; retirer `noindex` et la bannière si et seulement si le site devient réel.
5. Choisir hébergeur et domaine, HTTPS, puis refaire les contrôles (accessibilité, performance, navigateurs).
