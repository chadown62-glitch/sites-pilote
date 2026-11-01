# Atelier Démo — site vitrine de démonstration

> **Démonstration — entreprise fictive.** « Atelier Démo » n'existe pas. Ce dépôt est un pilote de production de site vitrine statique.

## Consulter le site
Aucune installation requise : ouvrir `index.html` dans un navigateur, ou lancer un serveur local :

```
python3 -m http.server 8000   # puis http://localhost:8000
```

## Contenu
- 7 pages commerciales : `index`, `entreprise`, `prestations`, `peinture`, `renovation-interieure`, `realisations`, `contact`
- 2 trames légales (à compléter) : `mentions-legales`, `confidentialite`
- `css/style.css`, `js/main.js` (menu mobile uniquement ; le formulaire est désactivé)

## Maintenance
Les `.html` sont générés par `python3 tools/build.py` (gabarit commun : en-tête, navigation, pied de page). Modifier le contenu dans `tools/build.py` puis relancer. Modifier directement les `.html` reste possible mais sera écrasé à la prochaine génération.

## Contrôles
`python3 tools/check.py` : liens internes, ancres, ressources externes, bannière, titre h1, motifs de secrets.

## Limites
Aucun contenu externe, traceur, cookie, base de données ni envoi de données. Le site n'est pas publié. Voir `PILOT_REPORT.md`.
