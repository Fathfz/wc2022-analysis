# Notebook Bilingual Markdown Template

Use this structure inside notebook markdown cells when you want to keep **French and English in the same notebook** without duplicating the whole file.

## Recommended GitHub-Friendly Pattern

```markdown
<details open>
<summary><strong>Français</strong></summary>

Texte en français.

</details>

<details>
<summary><strong>English</strong></summary>

English text.

</details>
```

## Why This Format

- It works well on GitHub because notebooks are rendered statically.
- It keeps a single notebook instead of two duplicated notebook versions.
- It makes updates easier because the code and outputs stay in one place.

## Suggested Usage

- Keep the code cells unchanged
- Translate only the markdown commentary
- Start with the most important notebooks first:
  - `02_final_match_eda_and_tactical_overview.ipynb`
  - `03_player_analysis  .ipynb`

## Example

```markdown
<details open>
<summary><strong>Français</strong></summary>

L'Argentine contrôle mieux la structure initiale du match, avec un milieu plus connecté et plusieurs relais entre les lignes.

</details>

<details>
<summary><strong>English</strong></summary>

Argentina controls the early structure of the match better, with a more connected midfield and multiple passing links between the lines.

</details>
```
