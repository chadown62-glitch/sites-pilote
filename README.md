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


## Contrôles reproductibles du pilote
Ce dépôt public ne doit contenir aucun dossier réel, échange de messagerie, accès
ou paiement. Les consignes techniques sont dans AGENTS.md.
Les observations privées de comptes et la configuration commerciale restent hors dépôt.
Aucun système de vente automatique n'est déployé par ces fichiers.

Contrôles locaux sans dépendance Python supplémentaire :
- python3 tools/check.py
- python3 tools/contrast.py
- python3 -m unittest discover -s tests -v
- python3 tools/package_demo.py
- python3 tools/preflight.py (code 2 attendu : aucun adaptateur opérationnel)

Le précontrôle peut lire une configuration locale privée fournie explicitement :
python3 tools/preflight.py /chemin/prive/configuration.json
Ne pas enregistrer cette configuration ni ses preuves dans le dépôt.
Ce script n'active aucune action, même si tous les champs sont renseignés.

Test navigateur : node tools/browser-check.cjs, uniquement si Playwright ET Chromium
sont déjà disponibles dans l'environnement. Aucun téléchargement/achat automatique.
Code 2 = non vérifié faute d'outil. Le site lui-même reste sans dépendance.
Le serveur éphémère du test écoute sur 127.0.0.1 et ne sert que les 11 fichiers du site.
Il n'est ni un aperçu distant ni un hébergement de production.

Le paquet out/atelier-demo.zip ne contient que les pages, le CSS et le JavaScript.
Les rapports, le générateur, les outils et la configuration restent hors paquet du pilote.
Une remise de sources maintenables pour un vrai projet a un périmètre distinct,
à définir et autoriser séparément.

La restauration du ZIP et une modification ciblée du générateur sont testées en
répertoire temporaire. Consulter PREPARATION_REPORT.md pour les résultats et limites.

## Tests du relais manuel (simulation locale)
Le précontrôle distingue payment_mode=manual (procédure manuelle authentifiée)
de payment_mode=automated (adaptateur authentifié). Aucun de ces réglages
n'active une action réelle. Les preuves et configurations restent hors dépôt.

Le module tools/payment_handoff.py produit uniquement un plan interne privé,
avec dédoublonnage à partir de clés déjà enregistrées fournies par l'appelant.
Il ne lit aucun mail, n'envoie aucune notification, ne valide aucune transaction,
ne stocke pas de dossier et n'autorise jamais une livraison. Un historique
indisponible bloque le plan ; il ne doit pas être remplacé par une liste vide.
La persistance privée et la liaison aux services restent à implémenter/tester.

Les tests de régression couvrent aussi l'historique de premier contact incohérent,
les formulaires ajoutés/actifs, scripts/styles embarqués, redirections meta
et liens vers des fichiers internes absents du paquet de site.
