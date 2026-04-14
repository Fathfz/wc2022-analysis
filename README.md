# Argentina vs France - World Cup Final 2022 Analysis

English | [Français](README.fr.md)

Football data storytelling project focused on the **2022 FIFA World Cup Final** between **Argentina** and **France**, built with Python, Jupyter notebooks, football event data, tactical interpretation, and visual analytics.

This repository is designed as both:
- a **portfolio project** in sports analytics,
- and a **publishable analysis workflow** that moves from context, to data preparation, to match interpretation, to player-level insights.

## Project Overview

This project explores a central question:

**How did Argentina control large phases of the 2022 World Cup Final, and how did France still manage to come back into the match?**

To answer it, the project combines:
- historical context before the final,
- match and tournament data preparation,
- team-level tactical analysis,
- player-level interpretation,
- exported visual storytelling assets,
- and a Streamlit application layer for presentation.

## Main Objectives

- Compare **Argentina's 4-3-3** and **France's 4-2-3-1**
- Study how game control, passing structure, and pressing shape the final
- Analyze shots, xG, momentum, recoveries, and passing networks
- Connect collective patterns with individual player performances
- Turn notebook-based work into a stronger GitHub and portfolio project

## Main Insights

- **Argentina controlled the initial structure of the match**, with a denser midfield and more stable passing connections.
- **France's first phase was more fragmented**, with circulation relying more heavily on the back line and the flanks.
- **The French comeback was driven by game-state changes and substitutions**, especially in a more vertical and chaotic phase.
- **Player-level analysis confirms the team-level reading**: Argentine midfielders were central to control, while France's safest passing profiles were often deeper.

## Repository Structure

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
   Historical context, FIFA rankings, head-to-head results, World Cup legacy, and pre-final positioning of both teams.

2. `01_data_collection_and_preparation.ipynb`  
   Data collection logic, filtering, final-match isolation, and preparation of the event data used throughout the project.

3. `02_final_match_eda_and_tactical_overview.ipynb`  
   Team-level tactical analysis of the final: xG, shots, pressure, recoveries, momentum, structures, and passing networks.

4. `03_player_analysis  .ipynb`  
   Player-level interpretation focused on passing, dribbling, shot profiles, pressure activity, movement, and tactical roles.

## Language Strategy

- The detailed notebooks are currently written in **French**
- The repository presentation is being made **bilingual**
- The next recommended step for the notebooks is **bilingual markdown cells** rather than full notebook duplication

Why this approach:
- it keeps a **single source of truth** for the analysis,
- it avoids maintaining two separate notebook versions,
- and it makes the repository easier to share with both French-speaking and English-speaking audiences.

A reusable bilingual markdown pattern is available in:
- [docs/NOTEBOOK_BILINGUAL_TEMPLATE.md](docs/NOTEBOOK_BILINGUAL_TEMPLATE.md)

## Visual Preview

![Global match dashboard](reports/figures/argentina_france_dashboard.png)

![Match momentum](reports/figures/momentum_match.png)

## Streamlit Application

A first Streamlit version is available in:
- `app/streamlit_app.py`

The app is designed to follow the same logic as the notebooks:
- historical context,
- data preparation,
- match-level tactical interpretation,
- player-level insights.

## Run The Project Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch the Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

Open the notebooks:

```bash
jupyter lab
```

## Data Sources

- StatsBomb Open Data
- Complementary historical football datasets stored in `data/raw/`
- Processed intermediate files stored in `data/processed/`

## Methodology Notes

- Match and extra time are analyzed separately from the penalty shootout.
- The penalty shootout is excluded from most tactical KPI shown in the project.
- The `Pressure` metric from StatsBomb is interpreted as an **event count**, not as a direct measure of pressing quality.
- The `xT` shown in the notebooks is a **simplified territorial-threat proxy**, not a full academic expected-threat model.

## Skills Demonstrated

- Python data analysis
- Jupyter notebook storytelling
- football event-data interpretation
- tactical reasoning
- data visualization
- GitHub project presentation
- Streamlit app structuring

## Project Status

- Notebook analysis: completed
- Markdown commentary: completed
- GitHub portfolio setup: in progress
- Bilingual repository documentation: in progress
- Streamlit application: V1 available

## Next Steps

- Finalize bilingual GitHub presentation
- Add bilingual markdown sections inside the notebooks
- Improve Streamlit polish and deployment readiness
- Prepare GitHub and LinkedIn sharing assets
