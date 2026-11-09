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


## Addendum de vérification indépendante — 1 novembre 2026
Le rapport ci-dessus décrit la première exécution de Claude. Lors de sa relecture,
le contrôleur original échoue sur le mot « secrets » dans README.md et dans ce
rapport, donc son succès final n'est pas reproductible sur ce commit d'origine.
Le contrôleur est corrigé et les résultats nouveaux sont dans PREPARATION_REPORT.md.
Les tests navigateur initiaux restent des résultats rapportés par Claude, non
réexécutés dans l'environnement de relecture faute de Chromium installé.
Les pages ont aussi été régénérées pour retirer les styles inline et préciser que
l'hébergeur éventuel peut traiter des journaux techniques. Refaire les tests
navigateur sur cette version avant toute utilisation réelle.


## Reprise du 2026-11-09 — test navigateur de la version régénérée
Point incomplet traité : les tests Chromium n'avaient pas été refaits sur la version régénérée.
Site non reconstruit ; aucun fichier de site modifié.
- `python3 tools/check.py` : OK (9 pages). `python3 -m unittest discover -s tests` : 40 tests OK.
- `node tools/browser-check.cjs` (Chromium/Playwright préinstallés, serveur local) : code de sortie 0 ;
  9 pages à 320, 375 et 1280 px ; 0 requête externe ; 0 erreur JavaScript ;
  clavier : réussi ; formulaire désactivé : réussi ; rendu sans JavaScript : réussi.
- Reste NON VÉRIFIÉ : lecteur d'écran, Firefox/Safari, appareils physiques, validateur HTML W3C,
  HTTPS/hébergeur réel, revue juridique. Aucune conformité n'est affirmée.
Les conditions avant publication réelle ci-dessus restent inchangées.
