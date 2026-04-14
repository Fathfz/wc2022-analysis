# Argentina vs France - World Cup Final 2022 Analysis

English | [Français](README.fr.md)

For many football fans, the **2022 World Cup Final** is the greatest final ever played.

Argentina seemed in control, then the match exploded. France came back from nowhere. **Kylian Mbappe** delivered a hat-trick. **Lionel Messi** finally lifted the World Cup with Argentina. The game swung from tactical control to pure chaos, and still ended with one of the most iconic images in football history.

That is exactly why this match is worth studying.

Beyond the emotion, the final raises a deeper analytical question:

**If France came back so violently, why did Argentina still look structurally superior for so much of the match?**

This repository answers that question through event data, tactical interpretation, visual storytelling, and player-level analysis.

## Why This Project Matters

This is not just a match recap.

It is a football analytics project built around a final that combined:
- a dominant opening phase from Argentina,
- a spectacular French comeback,
- extra-time tension,
- an Mbappe hat-trick,
- Messi's decisive influence,
- and a tactical story far richer than the final score alone.

The goal is to move from emotion to explanation:
- Who controlled the ball?
- Who controlled territory?
- Why did the match change?
- Which players carried those shifts?

## Core Question

This project is built around one central idea:

**Argentina and France did not threaten the final in the same way.**

Argentina controlled more of the structure:
- more continuity in passing,
- more stable midfield connections,
- more regular territorial progression,
- and a clearer collective framework.

France, however, stayed alive through rupture:
- direct attacks,
- explosive sequences,
- individual acceleration,
- and the extraordinary finishing impact of Mbappe.

The full analysis is therefore not just about who created more, but about **how each team created danger**.

## Analytical Architecture

The repository follows a clear progression from context to interpretation:

1. `00_context_and_historical_background cld.ipynb`  
   Sets the stage through historical context, FIFA ranking, head-to-head history, and pre-final tactical context.

2. `01_data_collection_and_preparation.ipynb`  
   Builds the analytical base by isolating the 2022 World Cup, filtering Argentina and France matches, and loading the event data of the final.

3. `02_final_match_eda_and_tactical_overview.ipynb`  
   This is the **collective core** of the project. It explains how the match evolved through:
   - event distribution,
   - shots and xG,
   - pressing and recoveries,
   - momentum and turning points,
   - passing structure,
   - and tactical reading of Argentina's 4-3-3 against France's 4-2-3-1.

4. `03_player_analysis  .ipynb`  
   This is the **individual core** of the project. It focuses on:
   - Messi vs Mbappe,
   - shot quality and finishing,
   - dribbling and attacking imbalance,
   - passing security,
   - player pass maps,
   - and the way individual profiles extend the collective story developed in notebook `02`.

## Why Notebooks 02 and 03 Matter Most

The real analytical heart of the project sits in notebooks `02` and `03`.

Notebook `02` explains the match as a tactical system:
- why Argentina controlled the early game,
- why France looked disconnected for long stretches,
- how substitutions changed the texture of the final,
- and why the match moved from Argentine control to end-game chaos.

Notebook `03` then asks the natural next question:
- if the collective patterns are real,
- which players actually embody them?

That is where the contrast becomes especially sharp:
- **Messi** appears as a player of continuity, connection, and decisive control,
- **Mbappe** appears as a player of rupture, acceleration, and violent finishing impact,
- and the rest of both squads help explain why Argentina looked more structured while France remained capable of sudden destruction.

## Main Insights

- **Argentina controlled more of the match structure**, especially through midfield density and passing continuity.
- **France did not dominate the game gradually**; it reshaped it through short, explosive, high-impact sequences.
- **The final changed nature after the 80th minute**, moving from controlled Argentine superiority to attacking chaos.
- **Messi and Mbappe symbolize two different kinds of influence**: one built on continuity and playmaking, the other on rupture and finishing violence.

## Repository Structure

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

## Language Note

- The repository presentation is bilingual
- The notebooks now include **French and English markdown sections**
- The code and outputs remain single-source, which keeps the analytical workflow consistent

## Visual Preview

![Global match dashboard](reports/figures/argentina_france_dashboard.png)

![Match momentum](reports/figures/momentum_match.png)

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
- Historical football datasets stored in `data/raw/`
- Processed intermediate files stored in `data/processed/`

## Methodology Notes

- Match and extra time are analyzed separately from the penalty shootout.
- The penalty shootout is excluded from the main tactical KPI.
- `Pressure` is treated as a StatsBomb event count, not as a direct measure of pressing quality.
- The `xT` used in the notebooks is a simplified territorial-threat proxy, not a full academic expected-threat model.
