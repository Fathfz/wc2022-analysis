from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "reports" / "figures"

TEAM_ORDER = ["Argentina", "France"]
TEAM_COLORS = {
    "Argentina": "#78AEE8",
    "France": "#1F4DB6",
    "Draw": "#B08D57",
}
PHASES = {
    "Match complet": (0, 120),
    "0-40 min - controle argentin": (0, 40),
    "41-78 min - ajustements francais": (41, 78),
    "79-120 min - retour et chaos": (79, 120),
}
PLAYER_IMAGE_MAP = {
    "Messi": "player_passmap_messi.png",
    "Mbappé": "player_passmap_mbappe.png",
    "Enzo": "player_passmap_enzo.png",
    "Griezmann": "player_passmap_griezmann.png",
}
PLAYER_NOTES = {
    "Messi": "Messi n'est pas seulement decisif. Il reste connecte aux circuits argentins et relie creation et finition.",
    "Mbappé": "Mbappe devient la principale sortie offensive francaise quand le match s'ouvre et que les transitions s'accelerent.",
    "Enzo": "Enzo est le meilleur symbole de la maitrise argentine : beaucoup de volume, de justesse et une forte centralite tactique.",
    "Griezmann": "Griezmann devait etre le lien du 4-2-3-1, mais son influence collective est moins structurante qu'attendu dans le reseau fort.",
    "Mac Allister": "Mac Allister densifie le cote gauche argentin et stabilise le lien entre le milieu et la largeur.",
    "Kolo Muani": "Kolo Muani change l'energie francaise par la profondeur, l'agressivite et une pression plus haute apres son entree.",
    "Tchouaméni": "Tchouameni apporte une base technique fiable, mais cela ne suffit pas a reconnecter toute la structure francaise.",
}


st.set_page_config(
    page_title="Argentina vs France - World Cup Final 2022",
    layout="wide",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(176,141,87,0.18), transparent 25%),
                    linear-gradient(180deg, #f7f3ea 0%, #efe7d7 100%);
            }
            h1, h2, h3 {
                font-family: Georgia, "Times New Roman", serif;
                color: #173225;
            }
            .hero {
                background: linear-gradient(135deg, #173225 0%, #24513d 65%, #b08d57 100%);
                color: #f8f3ea;
                padding: 2rem 2.1rem;
                border-radius: 26px;
                box-shadow: 0 22px 44px rgba(22, 51, 38, 0.16);
                margin-bottom: 1.2rem;
            }
            .hero h1 { color: #f8f3ea; margin-bottom: 0.35rem; }
            .hero-kicker {
                text-transform: uppercase;
                letter-spacing: 0.18em;
                font-size: 0.82rem;
                opacity: 0.8;
            }
            .badge {
                display: inline-block;
                margin: 0.25rem 0.4rem 0 0;
                padding: 0.32rem 0.72rem;
                border-radius: 999px;
                background: rgba(255,255,255,0.14);
                border: 1px solid rgba(255,255,255,0.2);
                font-size: 0.86rem;
            }
            .glass-card {
                background: rgba(255,255,255,0.78);
                border: 1px solid rgba(22,51,38,0.08);
                border-radius: 18px;
                padding: 1rem 1.05rem;
                box-shadow: 0 12px 28px rgba(22,51,38,0.08);
                min-height: 160px;
            }
            .card-title {
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: #617066;
                font-size: 0.74rem;
                margin-bottom: 0.5rem;
            }
            .card-value {
                font-size: 1.7rem;
                color: #173225;
                font-family: Georgia, "Times New Roman", serif;
                margin-bottom: 0.65rem;
            }
            .insight-card {
                background: rgba(255,255,255,0.76);
                border-left: 5px solid #b08d57;
                border-radius: 18px;
                padding: 1rem;
                box-shadow: 0 10px 24px rgba(22,51,38,0.05);
                min-height: 180px;
            }
            .sidebar-note {
                background: rgba(176,141,87,0.14);
                border-radius: 16px;
                padding: 0.95rem 1rem;
                line-height: 1.58;
                color: #173225;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_plot_style(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Arial", "color": "#173225"},
        margin={"l": 30, "r": 20, "t": 50, "b": 20},
        height=height,
        legend_title_text="",
    )
    return fig


def show_figure(filename: str, caption: str) -> None:
    path = FIGURES_DIR / filename
    if path.exists():
        st.image(str(path), caption=caption, use_column_width=True)
    else:
        st.warning(f"Figure introuvable : {filename}")


def fmt(value: float | int, digits: int = 0) -> str:
    if pd.isna(value):
        return "-"
    if digits == 0:
        return f"{int(round(float(value)))}"
    return f"{float(value):.{digits}f}"


def team_card(title: str, arg_value: str, fra_value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-title">{title}</div>
            <div class="card-value">ARG {arg_value} vs {fra_value} FRA</div>
            <div>{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def note_box(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <h4 style="margin-top:0; margin-bottom:0.5rem;">{title}</h4>
            <p style="margin:0;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_h2h() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_DIR / "h2h_arg_fra.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


@st.cache_data(show_spinner=False)
def load_wc_meetings() -> pd.DataFrame:
    df = pd.read_csv(PROCESSED_DIR / "wc_arg_vs_fra.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df.sort_values("Year")


@st.cache_data(show_spinner=False)
def load_rankings() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "rank.csv")
    return df[df["Team"].isin(TEAM_ORDER)].copy()


@st.cache_data(show_spinner=False)
def load_world_cups() -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / "world_cups.csv")


def prepare_route(path: Path, team: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["match_date"] = pd.to_datetime(df["match_date"])
    df = df.sort_values("match_date").reset_index(drop=True)
    df["stage"] = df["competition_stage"]
    df["opponent"] = np.where(df["home_team"] == team, df["away_team"], df["home_team"])
    df["goals_for"] = np.where(df["home_team"] == team, df["home_score"], df["away_score"])
    df["goals_against"] = np.where(df["home_team"] == team, df["away_score"], df["home_score"])
    df["result"] = np.select(
        [df["goals_for"] > df["goals_against"], df["goals_for"] < df["goals_against"]],
        ["Win", "Loss"],
        default="Draw",
    )
    df["scoreline"] = df["goals_for"].astype(str) + "-" + df["goals_against"].astype(str)
    return df


@st.cache_data(show_spinner=False)
def load_routes() -> tuple[pd.DataFrame, pd.DataFrame]:
    return (
        prepare_route(RAW_DIR / "argentina_matches.csv", "Argentina"),
        prepare_route(RAW_DIR / "france_matches.csv", "France"),
    )


@st.cache_data(show_spinner=False)
def load_events() -> pd.DataFrame:
    events = pd.read_csv(RAW_DIR / "events_finale.csv", low_memory=False)
    events["period"] = pd.to_numeric(events["period"], errors="coerce")
    events["minute"] = pd.to_numeric(events["minute"], errors="coerce").fillna(0)
    events["second"] = pd.to_numeric(events["second"], errors="coerce").fillna(0)
    events["minute_exact"] = events["minute"] + events["second"] / 60
    events["event_outcome"] = (
        events["shot_outcome"]
        .fillna(events["pass_outcome"])
        .fillna(events["duel_outcome"])
        .fillna(events["dribble_outcome"])
        .fillna(events["goalkeeper_outcome"])
    )
    return events


@st.cache_data(show_spinner=False)
def load_events_match_only() -> pd.DataFrame:
    return load_events()[load_events()["period"] != 5].copy()


@st.cache_data(show_spinner=False)
def load_pass_stats() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / "stats_passes_joueurs_finale.csv")


@st.cache_data(show_spinner=False)
def load_shot_stats() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / "stats_tirs_joueurs_finale.csv")


@st.cache_data(show_spinner=False)
def load_player_profiles() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DIR / "stats_joueurs_finale.csv").rename(
        columns={"taux_passes": "taux_passes_pct"}
    )


@st.cache_data(show_spinner=False)
def load_name_map() -> dict[str, str]:
    passes = load_pass_stats()[["player", "player_clean"]].drop_duplicates()
    shots = load_shot_stats()[["player", "player_clean"]].drop_duplicates()
    mapping = dict(zip(passes["player"], passes["player_clean"]))
    mapping.update(dict(zip(shots["player"], shots["player_clean"])))
    return mapping


def clean_player_label(name: str) -> str:
    mapping = load_name_map()
    if pd.isna(name):
        return "Unknown"
    return mapping.get(name, str(name).split()[-1])


def summarize_team_metrics(events: pd.DataFrame) -> dict[str, dict[str, float]]:
    shots = events[events["type"] == "Shot"].copy()
    shots["shot_statsbomb_xg"] = pd.to_numeric(
        shots["shot_statsbomb_xg"], errors="coerce"
    ).fillna(0.0)
    summary: dict[str, dict[str, float]] = {}
    for team in TEAM_ORDER:
        team_events = events[events["team"] == team]
        team_shots = shots[shots["team"] == team]
        team_passes = team_events[team_events["type"] == "Pass"]
        summary[team] = {
            "shots": int(len(team_shots)),
            "goals": int(team_shots["shot_outcome"].eq("Goal").sum()),
            "xg": float(team_shots["shot_statsbomb_xg"].sum()),
            "completed_passes": int(team_passes["pass_outcome"].isna().sum()),
            "pressures": int((team_events["type"] == "Pressure").sum()),
            "recoveries": int((team_events["type"] == "Ball Recovery").sum()),
        }
    distance_df = pd.read_csv(PROCESSED_DIR / "stats_equipes_finale.csv")
    for row in distance_df.itertuples(index=False):
        summary[row.team]["distance_km"] = float(row.volume_jeu_km)
    return summary


def get_phase_note(phase_label: str) -> str:
    notes = {
        "Match complet": "Vue globale du match : l'Argentine controle mieux la structure, la France revient quand la finale devient plus directe et plus chaotique.",
        "0-40 min - controle argentin": "Cette phase correspond au meilleur temps argentin : plus de controle positionnel, plus de continuite dans les circuits et un avantage net dans la construction.",
        "41-78 min - ajustements francais": "La France commence a modifier le rythme du match, mais l'Argentine garde encore une lecture collective plus propre avant la bascule totale.",
        "79-120 min - retour et chaos": "La finale change de nature : plus de transitions, plus de duels, plus de desordre. C'est la zone ideale pour le retour francais.",
    }
    return notes[phase_label]


def filter_events_by_minutes(events: pd.DataFrame, minute_range: tuple[int, int]) -> pd.DataFrame:
    start, end = minute_range
    return events[(events["minute_exact"] >= start) & (events["minute_exact"] <= end)].copy()


def make_h2h_results_chart(h2h: pd.DataFrame) -> go.Figure:
    results = h2h.copy()
    results["winner_label"] = results["Winning Team"].fillna("Draw").replace({"": "Draw"})
    counts = (
        results["winner_label"]
        .value_counts()
        .rename_axis("result")
        .reset_index(name="matches")
    )
    fig = px.bar(
        counts,
        x="result",
        y="matches",
        color="result",
        text="matches",
        color_discrete_map=TEAM_COLORS,
        category_orders={"result": ["Argentina", "France", "Draw"]},
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Nombre de matchs")
    return apply_plot_style(fig, height=360)


def make_titles_chart(world_cups: pd.DataFrame) -> go.Figure:
    rows = []
    for team in TEAM_ORDER:
        titles = int((world_cups["Winner"] == team).sum())
        finals = int(((world_cups["Winner"] == team) | (world_cups["Runners-Up"] == team)).sum())
        podiums = int(
            (
                (world_cups["Winner"] == team)
                | (world_cups["Runners-Up"] == team)
                | (world_cups["Third"] == team)
            ).sum()
        )
        rows.append({"team": team, "Titles": titles, "Finals": finals, "Podiums": podiums})
    df = pd.DataFrame(rows).melt(id_vars="team", var_name="metric", value_name="value")
    fig = px.bar(
        df,
        x="metric",
        y="value",
        color="team",
        barmode="group",
        color_discrete_map=TEAM_COLORS,
        text="value",
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Nombre")
    return apply_plot_style(fig, height=360)


def make_ranking_chart(rankings: pd.DataFrame) -> go.Figure:
    df = rankings.copy().sort_values("FIFA Ranking", ascending=False)
    fig = px.bar(
        df,
        x="FIFA Ranking",
        y="Team",
        orientation="h",
        color="Team",
        text="FIFA Ranking",
        color_discrete_map=TEAM_COLORS,
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="Classement FIFA (plus bas = meilleur)", autorange="reversed")
    fig.update_yaxes(title="")
    return apply_plot_style(fig, height=300)


def make_wc_meetings_chart(wc_meetings: pd.DataFrame) -> go.Figure:
    df = wc_meetings.copy()
    df["winner_label"] = df["Winning Team"].fillna("Draw").replace({"": "Draw"})
    df["scoreline"] = (
        df["Home Team"]
        + " "
        + df["Home Goals"].astype(str)
        + "-"
        + df["Away Goals"].astype(str)
        + " "
        + df["Away Team"]
    )
    fig = px.scatter(
        df,
        x="Year",
        y="Stage",
        color="winner_label",
        size=[18] * len(df),
        hover_name="scoreline",
        hover_data={"Date": True, "winner_label": True, "Year": True, "Stage": True},
        color_discrete_map=TEAM_COLORS,
    )
    fig.update_yaxes(title="")
    fig.update_xaxes(dtick=20)
    return apply_plot_style(fig, height=330)


def make_route_chart(route_df: pd.DataFrame, team: str) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(
        x=route_df["stage"],
        y=route_df["goals_for"],
        name="Buts marques",
        marker_color=TEAM_COLORS[team],
        customdata=np.stack([route_df["opponent"], route_df["scoreline"]], axis=-1),
        hovertemplate="%{x}<br>vs %{customdata[0]}<br>Score: %{customdata[1]}<extra></extra>",
    )
    fig.add_bar(
        x=route_df["stage"],
        y=route_df["goals_against"],
        name="Buts encaisses",
        marker_color="#B08D57",
        customdata=np.stack([route_df["opponent"], route_df["scoreline"]], axis=-1),
        hovertemplate="%{x}<br>vs %{customdata[0]}<br>Score: %{customdata[1]}<extra></extra>",
    )
    fig.update_layout(barmode="group")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Buts")
    return apply_plot_style(fig, height=350)


def make_event_types_chart(events: pd.DataFrame) -> go.Figure:
    counts = events["type"].value_counts().head(12).rename_axis("event_type").reset_index(name="count")
    fig = px.bar(
        counts,
        x="count",
        y="event_type",
        orientation="h",
        text="count",
        color_discrete_sequence=["#24513d"],
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="Occurrences")
    fig.update_yaxes(title="")
    return apply_plot_style(fig, height=430)


def make_event_flow_chart(events: pd.DataFrame) -> go.Figure:
    df = events.copy()
    df["minute_bin"] = (df["minute"] // 15) * 15
    flow = df.groupby(["minute_bin", "team"]).size().reset_index(name="events_count")
    fig = px.bar(
        flow,
        x="minute_bin",
        y="events_count",
        color="team",
        barmode="group",
        color_discrete_map=TEAM_COLORS,
    )
    fig.update_xaxes(title="Minute (groupes de 15 minutes)")
    fig.update_yaxes(title="Nombre d'evenements")
    return apply_plot_style(fig, height=360)


def make_cumulative_xg_chart(shots: pd.DataFrame) -> go.Figure:
    df = shots.copy().sort_values("minute_exact")
    df["shot_statsbomb_xg"] = pd.to_numeric(df["shot_statsbomb_xg"], errors="coerce").fillna(0.0)
    cumulative = []
    for team in TEAM_ORDER:
        team_df = df[df["team"] == team].copy()
        team_df["cumulative_xg"] = team_df["shot_statsbomb_xg"].cumsum()
        cumulative.append(team_df)
    plot_df = pd.concat(cumulative, ignore_index=True) if cumulative else pd.DataFrame()
    fig = px.line(
        plot_df,
        x="minute_exact",
        y="cumulative_xg",
        color="team",
        markers=True,
        color_discrete_map=TEAM_COLORS,
    )
    goals = df[df["shot_outcome"] == "Goal"].copy()
    if not goals.empty:
        fig.add_trace(
            go.Scatter(
                x=goals["minute_exact"],
                y=goals.groupby("team")["shot_statsbomb_xg"].cumsum(),
                mode="markers",
                marker={"size": 11, "symbol": "diamond", "color": "#B08D57"},
                name="Buts",
                text=[clean_player_label(name) for name in goals["player"]],
                hovertemplate="But: %{text}<br>Minute: %{x:.1f}<extra></extra>",
            )
        )
    fig.update_xaxes(title="Minute")
    fig.update_yaxes(title="xG cumule")
    return apply_plot_style(fig, height=360)


def make_shot_timeline_chart(shots: pd.DataFrame) -> go.Figure:
    df = shots.copy()
    df["shot_statsbomb_xg"] = pd.to_numeric(df["shot_statsbomb_xg"], errors="coerce").fillna(0.0)
    df["player_label"] = df["player"].apply(clean_player_label)
    df["is_goal"] = np.where(df["shot_outcome"] == "Goal", "But", "Tir")
    fig = px.scatter(
        df,
        x="minute_exact",
        y="team",
        size="shot_statsbomb_xg",
        color="team",
        symbol="is_goal",
        hover_name="player_label",
        hover_data={"shot_statsbomb_xg": ":.2f", "shot_outcome": True, "minute_exact": ":.1f"},
        color_discrete_map=TEAM_COLORS,
        size_max=28,
    )
    fig.update_xaxes(title="Minute")
    fig.update_yaxes(title="")
    return apply_plot_style(fig, height=330)


def make_top_passers_chart(pass_stats: pd.DataFrame, team: str) -> go.Figure:
    df = (
        pass_stats[pass_stats["team"] == team]
        .sort_values(["passes_tentees", "taux_passes_pct"], ascending=[False, False])
        .head(8)
        .sort_values("passes_tentees", ascending=True)
    )
    fig = px.bar(
        df,
        x="passes_tentees",
        y="player_clean",
        orientation="h",
        color_discrete_sequence=[TEAM_COLORS[team]],
        text="taux_passes_pct",
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="%{y}<br>Passes: %{x}<br>Reussite: %{text:.1f}%<extra></extra>",
    )
    fig.update_xaxes(title="Passes tentees")
    fig.update_yaxes(title="")
    return apply_plot_style(fig, height=360)


def make_pass_scatter_chart(pass_stats: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        pass_stats,
        x="passes_tentees",
        y="taux_passes_pct",
        color="team",
        hover_name="player_clean",
        size="passes_reussies",
        color_discrete_map=TEAM_COLORS,
        size_max=26,
    )
    fig.update_xaxes(title="Passes tentees")
    fig.update_yaxes(title="Taux de reussite (%)")
    return apply_plot_style(fig, height=380)


def make_top_pressure_chart(events: pd.DataFrame, team: str) -> go.Figure:
    pressure = events[(events["type"] == "Pressure") & (events["team"] == team)].copy()
    counts = (
        pressure["player"]
        .apply(clean_player_label)
        .value_counts()
        .head(8)
        .sort_values(ascending=True)
        .rename_axis("player")
        .reset_index(name="pressures")
    )
    fig = px.bar(
        counts,
        x="pressures",
        y="player",
        orientation="h",
        text="pressures",
        color_discrete_sequence=[TEAM_COLORS[team]],
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="Pressions")
    fig.update_yaxes(title="")
    return apply_plot_style(fig, height=360)


def make_top_recoveries_chart(events: pd.DataFrame, team: str) -> go.Figure:
    recoveries = events[(events["type"] == "Ball Recovery") & (events["team"] == team)].copy()
    counts = (
        recoveries["player"]
        .apply(clean_player_label)
        .value_counts()
        .head(8)
        .sort_values(ascending=True)
        .rename_axis("player")
        .reset_index(name="recoveries")
    )
    fig = px.bar(
        counts,
        x="recoveries",
        y="player",
        orientation="h",
        text="recoveries",
        color_discrete_sequence=[TEAM_COLORS[team]],
    )
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="Recuperations")
    fig.update_yaxes(title="")
    return apply_plot_style(fig, height=360)


def make_player_comparison_chart(profiles: pd.DataFrame, player: str) -> go.Figure:
    row = profiles[profiles["player"] == player].iloc[0]
    team_df = profiles[profiles["team"] == row["team"]]
    data = pd.DataFrame(
        {
            "metric": ["Passes", "Reussite %", "xG", "Dribbles reussis", "Volume km"] * 2,
            "series": [player] * 5 + ["Moyenne equipe"] * 5,
            "value": [
                row["passes_tentees"],
                row["taux_passes_pct"],
                row["xg_total"],
                row["dribbles_reussis"],
                row["volume_jeu_km"],
                team_df["passes_tentees"].mean(),
                team_df["taux_passes_pct"].mean(),
                team_df["xg_total"].mean(),
                team_df["dribbles_reussis"].mean(),
                team_df["volume_jeu_km"].mean(),
            ],
        }
    )
    fig = px.bar(
        data,
        x="metric",
        y="value",
        color="series",
        barmode="group",
        color_discrete_map={player: TEAM_COLORS[row["team"]], "Moyenne equipe": "#B08D57"},
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Valeur")
    return apply_plot_style(fig, height=360)


def make_top_players_chart(profiles: pd.DataFrame, metric: str, team_filter: str) -> go.Figure:
    labels = {
        "passes_tentees": "Passes tentees",
        "taux_passes_pct": "Reussite passe (%)",
        "xg_total": "xG total",
        "dribbles_reussis": "Dribbles reussis",
        "volume_jeu_km": "Volume de jeu (km)",
        "buts": "Buts",
    }
    df = profiles.copy()
    if team_filter != "Tous":
        df = df[df["team"] == team_filter]
    df = df.sort_values(metric, ascending=False).head(10).sort_values(metric, ascending=True)
    fig = px.bar(
        df,
        x=metric,
        y="player",
        orientation="h",
        color="team",
        color_discrete_map=TEAM_COLORS,
    )
    fig.update_xaxes(title=labels[metric])
    fig.update_yaxes(title="")
    return apply_plot_style(fig, height=400)


def make_star_duel_chart(profiles: pd.DataFrame) -> go.Figure:
    stars = profiles[profiles["player"].isin(["Messi", "Mbappé"])].copy()
    duel = pd.DataFrame(
        {
            "metric": ["Passes", "xG", "Tirs", "Buts", "Volume km"],
            "Messi": [
                float(stars.loc[stars["player"] == "Messi", "passes_tentees"].iloc[0]),
                float(stars.loc[stars["player"] == "Messi", "xg_total"].iloc[0]),
                float(stars.loc[stars["player"] == "Messi", "tirs"].iloc[0]),
                float(stars.loc[stars["player"] == "Messi", "buts"].iloc[0]),
                float(stars.loc[stars["player"] == "Messi", "volume_jeu_km"].iloc[0]),
            ],
            "Mbappé": [
                float(stars.loc[stars["player"] == "Mbappé", "passes_tentees"].iloc[0]),
                float(stars.loc[stars["player"] == "Mbappé", "xg_total"].iloc[0]),
                float(stars.loc[stars["player"] == "Mbappé", "tirs"].iloc[0]),
                float(stars.loc[stars["player"] == "Mbappé", "buts"].iloc[0]),
                float(stars.loc[stars["player"] == "Mbappé", "volume_jeu_km"].iloc[0]),
            ],
        }
    ).melt(id_vars="metric", var_name="player", value_name="value")
    fig = px.bar(
        duel,
        x="metric",
        y="value",
        color="player",
        barmode="group",
        color_discrete_map={"Messi": TEAM_COLORS["Argentina"], "Mbappé": TEAM_COLORS["France"]},
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Valeur")
    return apply_plot_style(fig, height=360)


def build_goal_list(shots: pd.DataFrame) -> list[str]:
    goals = shots[shots["shot_outcome"] == "Goal"].copy().sort_values("minute_exact")
    return [
        f"{int(row.minute_exact)}' - {clean_player_label(row.player)} ({row.team})"
        for row in goals.itertuples(index=False)
    ]


def render_intro(summary: dict[str, dict[str, float]]) -> None:
    st.markdown(
        """
        <section class="hero">
            <div class="hero-kicker">Football data storytelling</div>
            <h1>Argentina 3-3 France</h1>
            <p>
                Une application Streamlit qui reprend la logique des notebooks :
                d'abord le contexte historique, puis la preparation des donnees,
                ensuite la lecture tactique du match, et enfin l'analyse joueur par joueur.
            </p>
            <p>
                Les KPI affiches ici excluent volontairement la seance de tirs au but
                pour garder une lecture analytique propre du match et de la prolongation.
            </p>
            <span class="badge">00 Contexte</span>
            <span class="badge">01 Donnees</span>
            <span class="badge">02 Match</span>
            <span class="badge">03 Joueurs</span>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("## Snapshot")
    cols = st.columns(4)
    with cols[0]:
        team_card("Tirs", fmt(summary["Argentina"]["shots"]), fmt(summary["France"]["shots"]), "L'Argentine genere davantage de volume offensif sur 120 minutes.")
    with cols[1]:
        team_card("xG", fmt(summary["Argentina"]["xg"], 2), fmt(summary["France"]["xg"], 2), "L'avantage argentin reste leger mais coherent avec la structure du match.")
    with cols[2]:
        team_card("Pressions", fmt(summary["Argentina"]["pressures"]), fmt(summary["France"]["pressures"]), "Le volume seul ne suffit pas : la qualite du pressing se lit dans la coordination et les zones.")
    with cols[3]:
        team_card("Volume de jeu (km)", fmt(summary["Argentina"]["distance_km"], 2), fmt(summary["France"]["distance_km"], 2), "L'intensite collective soutient la maitrise argentine.")


def render_context_section() -> None:
    h2h = load_h2h()
    rankings = load_rankings()
    world_cups = load_world_cups()
    wc_meetings = load_wc_meetings()
    argentina_route, france_route = load_routes()

    st.markdown("## 00. Contexte historique")
    st.markdown(
        """
        Cette premiere section reprend la logique du notebook `00` :
        avant d'analyser la finale elle-meme, on replace le match dans une histoire plus large,
        faite de palmares, de confrontations directes, de contexte 2022 et de trajectoires vers la finale.
        """
    )

    tabs = st.tabs(["Historique global", "Coupe du Monde", "Parcours 2022"])
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_h2h_results_chart(h2h), use_container_width=True)
        with col2:
            st.plotly_chart(make_titles_chart(world_cups), use_container_width=True)
        col1, col2 = st.columns([0.9, 1.1])
        with col1:
            st.plotly_chart(make_ranking_chart(rankings), use_container_width=True)
        with col2:
            note_box(
                "Lecture",
                "Le contexte historique montre deux nations majeures, mais avec des points de depart differents : l'Argentine arrive avec un groupe 2022 mieux classe et une densite historique forte, tandis que la France vient defendre un titre mondial recent.",
            )
    with tabs[1]:
        st.plotly_chart(make_wc_meetings_chart(wc_meetings), use_container_width=True)
        st.markdown(
            """
            Les confrontations en Coupe du Monde donnent deja un recit : succes argentins en 1930 et 1978,
            puis victoire francaise spectaculaire en 2018. La finale 2022 s'inscrit donc dans une rivalite
            breve, mais symboliquement tres forte.
            """
        )
    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_route_chart(argentina_route, "Argentina"), use_container_width=True)
            st.dataframe(
                argentina_route[["stage", "opponent", "scoreline", "result"]].rename(
                    columns={"stage": "Tour", "opponent": "Adversaire", "scoreline": "Score", "result": "Resultat"}
                ),
                hide_index=True,
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(make_route_chart(france_route, "France"), use_container_width=True)
            st.dataframe(
                france_route[["stage", "opponent", "scoreline", "result"]].rename(
                    columns={"stage": "Tour", "opponent": "Adversaire", "scoreline": "Score", "result": "Resultat"}
                ),
                hide_index=True,
                use_container_width=True,
            )


def render_data_section(events: pd.DataFrame) -> None:
    match_events = events[events["period"] != 5].copy()

    st.markdown("## 01. Collecte et preparation des donnees")
    st.markdown(
        """
        Cette section reprend l'esprit du notebook `01` :
        quelles donnees sont chargees, comment la finale est isolee, et pourquoi certains filtres
        sont necessaires pour rendre l'analyse coherente.
        """
    )

    cols = st.columns(4)
    cols[0].metric("Evenements bruts finale", fmt(len(events)))
    cols[1].metric("Evenements analyses", fmt(len(match_events)))
    cols[2].metric("Types d'evenements", fmt(match_events["type"].nunique()))
    cols[3].metric("Equipes", "2")

    st.markdown(
        """
        **Choix de lecture :**
        le fichier brut de la finale contient **4407 evenements**.
        Pour les KPI tactiques affiches dans l'application, on conserve **4386 evenements**
        correspondant au match et a la prolongation, en excluant la seance de tirs au but.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_event_types_chart(match_events), use_container_width=True)
    with col2:
        st.plotly_chart(make_event_flow_chart(match_events), use_container_width=True)

    st.markdown("### Explorateur d'evenements")
    filter_col1, filter_col2, filter_col3 = st.columns([0.25, 0.25, 0.5])
    team_filter = filter_col1.selectbox("Equipe", ["Toutes"] + TEAM_ORDER)
    event_types = ["Tous"] + sorted(match_events["type"].dropna().unique().tolist())
    event_filter = filter_col2.selectbox("Type d'evenement", event_types)
    minute_range = filter_col3.slider("Plage de minutes", 0, 120, (0, 120))

    filtered = filter_events_by_minutes(match_events, minute_range)
    if team_filter != "Toutes":
        filtered = filtered[filtered["team"] == team_filter]
    if event_filter != "Tous":
        filtered = filtered[filtered["type"] == event_filter]

    preview = filtered[["minute", "team", "player", "type", "event_outcome", "possession_team"]].copy()
    preview["player"] = preview["player"].fillna("-").apply(clean_player_label)
    preview = preview.rename(
        columns={
            "minute": "Minute",
            "team": "Equipe",
            "player": "Joueur",
            "type": "Evenement",
            "event_outcome": "Outcome",
            "possession_team": "Equipe en possession",
        }
    )
    st.dataframe(preview.head(80), hide_index=True, use_container_width=True)


def render_match_section(events_match: pd.DataFrame, pass_stats: pd.DataFrame) -> None:
    st.markdown("## 02. Lecture globale du match")
    st.markdown(
        """
        Le notebook `02` montrait deja une idee forte :
        l'Argentine controle mieux la structure du match, alors que la France devient plus dangereuse
        a mesure que la finale se verticalise. L'application garde cette logique, mais la rend plus interactive.
        """
    )

    tabs = st.tabs(["Chronologie", "Possession et pressing", "Structures tactiques"])
    with tabs[0]:
        phase_choice = st.selectbox("Choisir une phase de lecture", list(PHASES.keys()))
        phase_events = filter_events_by_minutes(events_match, PHASES[phase_choice])
        phase_shots = phase_events[phase_events["type"] == "Shot"].copy()
        phase_summary = summarize_team_metrics(phase_events)

        st.markdown(get_phase_note(phase_choice))
        cols = st.columns(4)
        with cols[0]:
            team_card("Tirs", fmt(phase_summary["Argentina"]["shots"]), fmt(phase_summary["France"]["shots"]), "Le volume de tirs aide a lire qui impose le plus souvent la menace.")
        with cols[1]:
            team_card("xG", fmt(phase_summary["Argentina"]["xg"], 2), fmt(phase_summary["France"]["xg"], 2), "Le xG resitue la qualite des situations creees dans cette seule phase.")
        with cols[2]:
            team_card("Passes completes", fmt(phase_summary["Argentina"]["completed_passes"]), fmt(phase_summary["France"]["completed_passes"]), "Un bon indicateur de maitrise structurelle dans la plage choisie.")
        with cols[3]:
            team_card("Pressions", fmt(phase_summary["Argentina"]["pressures"]), fmt(phase_summary["France"]["pressures"]), "Le volume de pression doit toujours etre complete par la lecture tactique.")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_cumulative_xg_chart(phase_shots), use_container_width=True)
        with col2:
            st.plotly_chart(make_shot_timeline_chart(phase_shots), use_container_width=True)

        goals = build_goal_list(phase_shots)
        if goals:
            st.markdown("**Buts dans cette phase**")
            for item in goals:
                st.markdown(f"- {item}")
    with tabs[1]:
        team_view = st.radio("Lecture par equipe", TEAM_ORDER, horizontal=True)
        top_passer = (
            pass_stats[pass_stats["team"] == team_view]
            .sort_values(["passes_tentees", "taux_passes_pct"], ascending=[False, False])
            .iloc[0]
        )
        st.markdown(
            f"""
            Cote **{team_view}**, le joueur qui tente le plus de passes est
            **{top_passer["player_clean"]}** avec **{fmt(top_passer["passes_tentees"])} passes**.
            Ce point est important, car il aide a savoir si la maitrise vient de la defense seule
            ou si elle traverse aussi le milieu et les zones plus hautes.
            """
        )
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_pass_scatter_chart(pass_stats), use_container_width=True)
        with col2:
            st.plotly_chart(make_top_passers_chart(pass_stats, team_view), use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_top_pressure_chart(events_match, team_view), use_container_width=True)
        with col2:
            st.plotly_chart(make_top_recoveries_chart(events_match, team_view), use_container_width=True)
        st.markdown(
            """
            La difference importante mise en avant dans les notebooks reste visible :
            l'Argentine relie mieux ses lignes et fait vivre son milieu, alors que la France
            accumule aussi des pressions et des interventions de reaction plus basses dans sa structure.
            """
        )
    with tabs[2]:
        st.markdown(
            """
            Les reseaux de passes affiches ci-dessous ne representent pas toutes les passes du match.
            Ils ne montrent que les connexions repetees **plus de 5 fois** afin de faire ressortir
            les vrais circuits collectifs.

            L'Argentine se lit comme un **4-3-3** plus dense et plus connecte, avec Enzo, De Paul
            et Mac Allister au coeur du jeu. La France se lit comme un **4-2-3-1** plus fragmente,
            ou la relance part souvent de la ligne defensive avant de chercher les couloirs.
            """
        )
        col1, col2 = st.columns(2)
        with col1:
            show_figure("passmap_team_Argentina.png", "Reseau de passes - Argentine")
        with col2:
            show_figure("passmap_team_France.png", "Reseau de passes - France")
        col1, col2 = st.columns(2)
        with col1:
            show_figure("positions_Argentina.png", "Structure moyenne - Argentine")
        with col2:
            show_figure("positions_France.png", "Structure moyenne - France")
        show_figure("zones_pression_comparison.png", "Comparaison des zones de pression")


def render_players_section(profiles: pd.DataFrame) -> None:
    st.markdown("## 03. Analyse individuelle")
    st.markdown(
        """
        Cette derniere section reprend la logique du notebook `03` :
        les performances individuelles ne sont pas lues isolees, mais comme le prolongement
        des tendances collectives deja observees dans le match.
        """
    )

    tabs = st.tabs(["Focus joueur", "Leaderboards", "Messi vs Mbappé"])
    with tabs[0]:
        team_filter = st.selectbox("Equipe", TEAM_ORDER, index=0)
        player_options = profiles[profiles["team"] == team_filter]["player"].tolist()
        default_index = player_options.index("Messi") if team_filter == "Argentina" and "Messi" in player_options else 0
        if team_filter == "France" and "Mbappé" in player_options:
            default_index = player_options.index("Mbappé")
        player = st.selectbox("Joueur", player_options, index=default_index)
        row = profiles[profiles["player"] == player].iloc[0]

        metric_cols = st.columns(5)
        metric_cols[0].metric("Passes", fmt(row["passes_tentees"]))
        metric_cols[1].metric("Reussite passe", f"{fmt(row['taux_passes_pct'], 1)} %")
        metric_cols[2].metric("xG", fmt(row["xg_total"], 2))
        metric_cols[3].metric("Dribbles reussis", fmt(row["dribbles_reussis"]))
        metric_cols[4].metric("Volume de jeu", f"{fmt(row['volume_jeu_km'], 2)} km")

        col1, col2 = st.columns([1.05, 0.95])
        with col1:
            st.plotly_chart(make_player_comparison_chart(profiles, player), use_container_width=True)
        with col2:
            show_figure(PLAYER_IMAGE_MAP.get(player, "player_passing_efficiency.png"), f"Visualisation associee - {player}")
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="card-title">Lecture tactique</div>
                    <div class="card-value" style="font-size:1.4rem;">{player}</div>
                    <div><strong>Equipe :</strong> {row["team"]}</div>
                    <div><strong>Tirs :</strong> {fmt(row["tirs"])} | <strong>Buts :</strong> {fmt(row["buts"])}</div>
                    <div style="margin-top:0.7rem;">{PLAYER_NOTES.get(player, "Profil important de la finale.")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with tabs[1]:
        team_scope = st.selectbox("Filtrer les leaderboards", ["Tous"] + TEAM_ORDER, index=0)
        metric = st.selectbox(
            "Choisir un indicateur",
            ["passes_tentees", "taux_passes_pct", "xg_total", "dribbles_reussis", "volume_jeu_km", "buts"],
            format_func=lambda x: {
                "passes_tentees": "Passes tentees",
                "taux_passes_pct": "Reussite a la passe",
                "xg_total": "xG total",
                "dribbles_reussis": "Dribbles reussis",
                "volume_jeu_km": "Volume de jeu",
                "buts": "Buts",
            }[x],
        )
        st.plotly_chart(make_top_players_chart(profiles, metric, team_scope), use_container_width=True)
        st.dataframe(
            profiles.sort_values(metric, ascending=False)
            .head(12)[["player", "team", metric]]
            .rename(columns={"player": "Joueur", "team": "Equipe", metric: "Valeur"}),
            hide_index=True,
            use_container_width=True,
        )
    with tabs[2]:
        st.plotly_chart(make_star_duel_chart(profiles), use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            show_figure("messi_vs_mbappe_bars.png", "Comparaison directe")
            show_figure("player_heatmap_messi_mbappe.png", "Heatmaps comparees")
        with col2:
            show_figure("player_convexhull_messi_mbappe.png", "Zones d'influence")
            show_figure("player_shotmap_messi_mbappe.png", "Shotmaps comparees")


def render_method_section() -> None:
    st.markdown("## Methodologie")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="glass-card">
                <div class="card-title">Sources</div>
                <div>- StatsBomb Open Data pour les evenements de la finale</div>
                <div>- Jeux de donnees historiques stockes dans <code>data/raw/</code></div>
                <div>- Figures exportees depuis les notebooks dans <code>reports/figures/</code></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="glass-card">
                <div class="card-title">Choix analytiques</div>
                <div>- la seance de tirs au but est exclue des KPI</div>
                <div>- les reseaux de passes gardent seulement les connexions > 5</div>
                <div>- le xT des notebooks est un proxy simplifie, pas un modele academique complet</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st.expander("Definitions utiles"):
        st.markdown(
            """
            - **Pressure** : dans les donnees StatsBomb, c'est un evenement de pression sur le porteur, pas une note de qualite du pressing.
            - **xT** : dans ce projet, il s'agit d'un score simplifie de menace territoriale fonde sur la progression horizontale.
            - **Lecture des reseaux** : les lignes n'affichent pas toutes les passes, seulement les relations repetees plus de 5 fois.
            """
        )


def main() -> None:
    inject_styles()
    events = load_events()
    events_match = load_events_match_only()
    pass_stats = load_pass_stats()
    profiles = load_player_profiles()
    summary = summarize_team_metrics(events_match)

    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Choisir une section",
        ["Accueil", "00 - Contexte historique", "01 - Donnees et preparation", "02 - Analyse du match", "03 - Analyse des joueurs", "Methodologie"],
    )
    st.sidebar.markdown(
        """
        <div class="sidebar-note">
            Cette application suit la chronologie des notebooks et transforme leur contenu
            en une lecture plus dynamique, plus claire et plus presentable pour GitHub,
            Streamlit et le portfolio.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.caption("Argentina vs France - World Cup Final 2022")

    if section == "Accueil":
        render_intro(summary)
        col1, col2, col3 = st.columns(3)
        with col1:
            note_box("00 - Contexte", "Comprendre le palmares, les confrontations directes et le parcours des deux equipes avant la finale.")
        with col2:
            note_box("01 - Donnees", "Voir comment la finale est isolee, pourquoi certains filtres comptent et a quoi ressemble la matiere premiere analytique.")
        with col3:
            note_box("02-03 - Match et joueurs", "Suivre le match, puis descendre au niveau des individus pour verifier ou nuancer les conclusions collectives.")
        show_figure("argentina_france_dashboard.png", "Apercu visuel du projet")
    elif section == "00 - Contexte historique":
        render_context_section()
    elif section == "01 - Donnees et preparation":
        render_data_section(events)
    elif section == "02 - Analyse du match":
        render_match_section(events_match, pass_stats)
    elif section == "03 - Analyse des joueurs":
        render_players_section(profiles)
    else:
        render_method_section()


if __name__ == "__main__":
    main()
