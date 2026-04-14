# Analyse Argentine vs France - Finale Coupe du Monde 2022

[English](README.md) | Français

Projet de data storytelling football centré sur la **finale de la Coupe du Monde 2022** entre **l'Argentine** et **la France**, construit avec Python, des notebooks Jupyter, des données événementielles de match, une lecture tactique, et des visualisations.

Ce dépôt est pensé à la fois comme :
- un **projet portfolio** en sports analytics,
- et une **analyse publiable** allant du contexte historique à l'interprétation joueur par joueur.

## Vue d'ensemble du projet

Le projet cherche à répondre à une question centrale :

**Comment l'Argentine a-t-elle contrôlé de larges séquences de la finale, et comment la France a-t-elle malgré tout réussi à revenir ?**

Pour y répondre, le projet combine :
- le contexte historique avant la finale,
- la préparation des données du tournoi et du match,
- une analyse tactique collective,
- une lecture individuelle des joueurs,
- des visuels exportés,
- et une couche Streamlit pour la présentation.

## Objectifs principaux

- Comparer le **4-3-3 argentin** et le **4-2-3-1 français**
- Étudier comment la maîtrise du jeu, la structure des passes et le pressing façonnent la finale
- Analyser les tirs, le xG, le momentum, les récupérations et les réseaux de passes
- Relier les tendances collectives aux performances individuelles
- Transformer un travail de notebooks en un projet GitHub plus fort pour le portfolio

## Enseignements clés

- **L'Argentine contrôle mieux la structure initiale du match**, avec un milieu plus dense et des connexions plus stables.
- **La première phase française est plus fragmentée**, avec une circulation davantage portée par la ligne défensive et les côtés.
- **Le retour français vient surtout du changement de dynamique du match et des entrées**, dans une phase plus verticale et plus chaotique.
- **L'analyse individuelle prolonge l'analyse collective** : les milieux argentins portent la maîtrise, tandis que les profils français les plus sûrs à la passe sont souvent plus bas.

## Structure du dépôt

```text
wc2022-analysis/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── processed/
│   └── raw/
├── notebooks/
│   ├── 00_context_and_historical_background cld.ipynb
│   ├── 01_data_collection_and_preparation.ipynb
│   ├── 02_final_match_eda_and_tactical_overview.ipynb
│   └── 03_player_analysis  .ipynb
├── reports/
│   └── figures/
├── docs/
│   └── NOTEBOOK_BILINGUAL_TEMPLATE.md
├── requirements.txt
├── README.md
└── README.fr.md
```

## Notebooks

1. `00_context_and_historical_background cld.ipynb`  
   Contexte historique, classement FIFA, confrontations directes, héritage en Coupe du Monde, et positionnement des deux équipes avant la finale.

2. `01_data_collection_and_preparation.ipynb`  
   Logique de collecte, filtrage, isolation de la finale, et préparation des données événementielles utilisées dans le projet.

3. `02_final_match_eda_and_tactical_overview.ipynb`  
   Analyse collective de la finale : xG, tirs, pressions, récupérations, momentum, structures et réseaux de passes.

4. `03_player_analysis  .ipynb`  
   Lecture individuelle des joueurs à travers les passes, dribbles, tirs, activités défensives, zones d'influence et rôles tactiques.

## Stratégie linguistique

- Les notebooks détaillés sont actuellement en **français**
- La présentation du dépôt devient progressivement **bilingue**
- La prochaine étape recommandée pour les notebooks est l'ajout de **cellules markdown bilingues**, plutôt qu'une duplication complète des notebooks

Pourquoi ce choix :
- il permet de garder une **seule source de vérité** pour l'analyse,
- il évite de maintenir deux versions complètes en parallèle,
- et il rend le dépôt plus simple à partager avec un public francophone et anglophone.

Un modèle réutilisable est disponible ici :
- [docs/NOTEBOOK_BILINGUAL_TEMPLATE.md](docs/NOTEBOOK_BILINGUAL_TEMPLATE.md)

## Aperçu visuel

![Dashboard global du match](reports/figures/argentina_france_dashboard.png)

![Momentum du match](reports/figures/momentum_match.png)

## Application Streamlit

Une première version de l'application Streamlit est disponible dans :
- `app/streamlit_app.py`

L'application suit la même logique que les notebooks :
- contexte historique,
- préparation des données,
- lecture tactique du match,
- analyse individuelle.

## Lancer le projet en local

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer l'application Streamlit :

```bash
streamlit run app/streamlit_app.py
```

Ouvrir les notebooks :

```bash
jupyter lab
```

## Sources de données

- StatsBomb Open Data
- Jeux de données historiques complémentaires stockés dans `data/raw/`
- Fichiers intermédiaires préparés dans `data/processed/`

## Notes méthodologiques

- Le match et la prolongation sont analysés séparément de la séance de tirs au but.
- La séance de tirs au but est exclue de la plupart des KPI tactiques affichés.
- La métrique `Pressure` de StatsBomb est interprétée comme un **compte d'événements**, et non comme une mesure directe de la qualité du pressing.
- Le `xT` utilisé dans les notebooks est un **proxy simplifié de menace territoriale**, et non un modèle académique complet.

## Compétences mobilisées

- analyse de données en Python
- storytelling avec notebooks Jupyter
- interprétation de données événementielles football
- raisonnement tactique
- visualisation de données
- présentation de projet sur GitHub
- structuration d'une application Streamlit

## État du projet

- Analyse notebook : terminée
- Commentaires markdown : terminés
- Mise en forme GitHub : en cours
- Documentation bilingue : en cours
- Application Streamlit : V1 disponible

## Prochaines étapes

- Finaliser la présentation bilingue GitHub
- Ajouter des blocs markdown bilingues dans les notebooks
- Améliorer le polish et le déploiement de l'application Streamlit
- Préparer le partage GitHub et LinkedIn
