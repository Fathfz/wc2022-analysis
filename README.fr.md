# Analyse Argentine vs France - Finale Coupe du Monde 2022

[English](README.md) | Français

Pour beaucoup de passionnés, la **finale de la Coupe du Monde 2022** est la plus grande finale de l'histoire.

L'Argentine semblait contrôler le match, puis tout a explosé. La France est revenue de presque nulle part. **Kylian Mbappé** a signé un triplé. **Lionel Messi** a enfin soulevé la Coupe du Monde avec l'Argentine. La rencontre est passée d'une lecture tactique très structurée à un chaos total, avant de se refermer sur l'une des images les plus fortes de l'histoire du football.

C'est précisément pour cela que ce match mérite une analyse.

Au-delà de l'émotion, cette finale pose une question plus profonde :

**Si la France est revenue avec une telle violence, pourquoi l'Argentine a-t-elle malgré tout semblé structurellement supérieure pendant une grande partie du match ?**

Ce dépôt cherche à répondre à cette question à travers les données événementielles, la lecture tactique, le storytelling visuel et l'analyse individuelle.

## Pourquoi ce projet compte

Ce projet n'est pas un simple résumé de match.

Il s'agit d'un travail de football analytics construit autour d'une finale qui a réuni :
- une entame argentine dominante,
- une remontée française spectaculaire,
- une tension énorme en prolongation,
- un triplé de Mbappé,
- le sacre final de Messi avec sa sélection,
- et une richesse tactique bien plus grande que ne le dit le score seul.

L'objectif est de passer de l'émotion à l'explication :
- Qui a contrôlé le ballon ?
- Qui a contrôlé le territoire ?
- Pourquoi le match a-t-il basculé ?
- Quels joueurs ont porté ces renversements ?

## Problématique centrale

Le projet repose sur une idée simple :

**L'Argentine et la France n'ont pas menacé cette finale de la même manière.**

L'Argentine a contrôlé davantage la structure du match :
- plus de continuité dans la passe,
- un milieu plus dense et plus connecté,
- une progression territoriale plus régulière,
- et un cadre collectif plus lisible.

La France, elle, est restée vivante par la rupture :
- attaques plus directes,
- séquences explosives,
- accélérations individuelles,
- et impact exceptionnel de Mbappé à la finition.

L'analyse complète ne cherche donc pas seulement à savoir qui a le plus créé, mais surtout **comment chaque équipe a créé du danger**.

## Architecture de l'analyse

Le dépôt suit une progression claire, du contexte jusqu'à l'interprétation :

1. `00_context_and_historical_background cld.ipynb`  
   Pose le décor avec le contexte historique, le classement FIFA, les confrontations directes et le cadre pré-finale.

2. `01_data_collection_and_preparation.ipynb`  
   Construit la base analytique en isolant la Coupe du Monde 2022, les matchs de l'Argentine et de la France, puis les événements détaillés de la finale.

3. `02_final_match_eda_and_tactical_overview.ipynb`  
   C'est le **cœur collectif** du projet. On y explique le match à travers :
   - la structure des événements,
   - les tirs et le xG,
   - le pressing et les récupérations,
   - le momentum et les bascules temporelles,
   - la structure de passe,
   - et la lecture tactique du 4-3-3 argentin face au 4-2-3-1 français.

4. `03_player_analysis  .ipynb`  
   C'est le **cœur individuel** du projet. On y étudie :
   - Messi vs Mbappé,
   - la qualité des tirs et la finition,
   - le dribble et la création de déséquilibre,
   - la sécurité technique à la passe,
   - les pass maps individuelles,
   - et la manière dont les profils joueurs prolongent l'histoire collective développée dans le notebook `02`.

## Pourquoi les notebooks 02 et 03 sont les plus importants

Le vrai centre analytique du projet se trouve dans les notebooks `02` et `03`.

Le notebook `02` explique le match comme un système tactique :
- pourquoi l'Argentine contrôle le début de rencontre,
- pourquoi la France paraît longtemps plus fragmentée,
- comment les changements modifient la texture du match,
- et pourquoi la finale passe d'un contrôle argentin à un chaos offensif.

Le notebook `03` pose ensuite la question naturelle :
- si les structures collectives sont réelles,
- quels joueurs les incarnent concrètement ?

C'est là que le contraste devient particulièrement fort :
- **Messi** apparaît comme un joueur de continuité, de liaison et de maîtrise,
- **Mbappé** comme un joueur de rupture, d'accélération et de violence offensive,
- et les autres profils permettent d'expliquer pourquoi l'Argentine paraît plus structurée, tandis que la France reste capable de détruire le cadre en quelques instants.

## Enseignements clés

- **L'Argentine a mieux contrôlé la structure du match**, surtout grâce à la densité de son milieu et à la continuité de sa circulation.
- **La France n'a pas repris le contrôle progressivement** ; elle a transformé le match par des séquences courtes, explosives et à très fort impact.
- **La finale change de nature après la 80e minute**, en passant d'une supériorité argentine maîtrisée à un chaos offensif presque total.
- **Messi et Mbappé symbolisent deux formes d'influence différentes** : l'une fondée sur la continuité et la création, l'autre sur la rupture et la finition.

## Structure du dépôt

```text
wc2022-analysis/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── processed/
│   └── raw/
├── docs/
│   └── NOTEBOOK_BILINGUAL_TEMPLATE.md
├── notebooks/
│   ├── 00_context_and_historical_background cld.ipynb
│   ├── 01_data_collection_and_preparation.ipynb
│   ├── 02_final_match_eda_and_tactical_overview.ipynb
│   └── 03_player_analysis  .ipynb
├── reports/
│   └── figures/
├── requirements.txt
├── README.md
└── README.fr.md
```

## Note sur la langue

- La présentation du dépôt est bilingue
- Les notebooks contiennent désormais des sections markdown en **français et en anglais**
- Le code et les outputs restent uniques, ce qui permet de conserver une logique analytique cohérente

## Aperçu visuel

![Dashboard global du match](reports/figures/argentina_france_dashboard.png)

![Momentum du match](reports/figures/momentum_match.png)

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
- Jeux de données historiques stockés dans `data/raw/`
- Fichiers intermédiaires préparés dans `data/processed/`

## Notes méthodologiques

- Le match et la prolongation sont analysés séparément de la séance de tirs au but.
- La séance de tirs au but est exclue des principaux KPI tactiques.
- `Pressure` est interprété comme un compte d'événements StatsBomb, et non comme une mesure directe de la qualité du pressing.
- Le `xT` utilisé dans les notebooks est un proxy simplifié de menace territoriale, et non un modèle académique complet.
