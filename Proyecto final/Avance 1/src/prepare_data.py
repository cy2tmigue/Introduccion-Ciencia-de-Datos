from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
CLEAN_DIR = PROJECT_DIR / "data" / "clean"

REQUIRED_FILES = [
    "awards.csv",
    "award_winners.csv",
    "confederations.csv",
    "goals.csv",
    "matches.csv",
    "players.csv",
    "player_appearances.csv",
    "squads.csv",
    "stadiums.csv",
    "teams.csv",
    "tournaments.csv",
]


def read_csv(name: str) -> pd.DataFrame:
    path = RAW_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero: python src/download_data.py"
        )
    df = pd.read_csv(path, low_memory=False)
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].astype("string").str.strip()
    return df


def save(df: pd.DataFrame, table_name: str) -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    output = CLEAN_DIR / f"{table_name}.csv"
    df.to_csv(output, index=False)
    print(f"[OK] {table_name:18s} {len(df):>7} filas -> {output.name}")


def require_columns(df: pd.DataFrame, columns: list[str], dataset: str) -> None:
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"{dataset}: faltan columnas requeridas: {missing}")


def main() -> None:
    print("Preparando y normalizando datos para las 15 tablas del Avance 1...\n")

    for filename in REQUIRED_FILES:
        if not (RAW_DIR / filename).exists():
            raise FileNotFoundError(
                f"Falta {filename}. Ejecuta primero: python src/download_data.py"
            )

    awards = read_csv("awards.csv")
    award_winners = read_csv("award_winners.csv")
    confederations = read_csv("confederations.csv")
    goals = read_csv("goals.csv")
    matches = read_csv("matches.csv")
    players = read_csv("players.csv")
    player_appearances = read_csv("player_appearances.csv")
    squads = read_csv("squads.csv")
    stadiums = read_csv("stadiums.csv")
    teams = read_csv("teams.csv")
    tournaments = read_csv("tournaments.csv")

    # ------------------------------------------------------------------
    # Tablas maestras: confederation, region, country y federation
    # ------------------------------------------------------------------
    conf_cols = [
        "confederation_id",
        "confederation_name",
        "confederation_code",
        "confederation_wikipedia_link",
    ]
    require_columns(confederations, conf_cols, "confederations.csv")
    confederation = (
        confederations[conf_cols]
        .drop_duplicates(subset=["confederation_id"])
        .sort_values("confederation_id")
    )

    require_columns(
        teams,
        [
            "team_id",
            "team_name",
            "team_code",
            "federation_name",
            "region_name",
            "confederation_id",
        ],
        "teams.csv",
    )
    require_columns(stadiums, ["stadium_id", "city_name", "country_name"], "stadiums.csv")

    team_region = (
        teams[["team_name", "region_name"]]
        .dropna(subset=["team_name"])
        .drop_duplicates(subset=["team_name"])
        .set_index("team_name")["region_name"]
        .to_dict()
    )

    country_names = sorted(
        set(teams["team_name"].dropna().tolist())
        | set(stadiums["country_name"].dropna().tolist())
        | set(matches["country_name"].dropna().tolist())
    )

    country_rows = []
    unknown_needed = False
    for country_name in country_names:
        region_name = team_region.get(country_name)
        if pd.isna(region_name) or region_name is None:
            region_name = "Unknown"
            unknown_needed = True
        country_rows.append({"country_name": country_name, "region_name": region_name})

    region_names = sorted(set(teams["region_name"].dropna().tolist()))
    if unknown_needed and "Unknown" not in region_names:
        region_names.append("Unknown")

    region = pd.DataFrame(
        [{"region_id": i + 1, "region_name": name} for i, name in enumerate(region_names)]
    )
    region_map = dict(zip(region["region_name"], region["region_id"]))

    country = pd.DataFrame(country_rows)
    country["region_id"] = country["region_name"].map(region_map)
    country = country.sort_values("country_name").reset_index(drop=True)
    country.insert(0, "country_id", range(1, len(country) + 1))
    country = country[["country_id", "country_name", "region_id"]]
    country_map = dict(zip(country["country_name"], country["country_id"]))

    fed_cols = [
        "federation_name",
        "team_name",
        "confederation_id",
        "federation_wikipedia_link",
    ]
    require_columns(teams, fed_cols, "teams.csv")
    federation = teams[fed_cols].dropna(subset=["federation_name"]).copy()
    federation["country_id"] = federation["team_name"].map(country_map)
    federation = (
        federation.sort_values(["federation_name", "team_name"])
        .drop_duplicates(subset=["federation_name"])
        .reset_index(drop=True)
    )
    federation.insert(0, "federation_id", range(1, len(federation) + 1))
    federation = federation[
        [
            "federation_id",
            "federation_name",
            "country_id",
            "confederation_id",
            "federation_wikipedia_link",
        ]
    ]
    federation_map = dict(zip(federation["federation_name"], federation["federation_id"]))

    # ------------------------------------------------------------------
    # team
    # ------------------------------------------------------------------
    team_cols = [
        "team_id",
        "team_name",
        "team_code",
        "mens_team",
        "womens_team",
        "federation_name",
        "confederation_id",
        "mens_team_wikipedia_link",
        "womens_team_wikipedia_link",
    ]
    require_columns(teams, team_cols, "teams.csv")
    team = teams[team_cols].drop_duplicates(subset=["team_id"]).copy()
    team["country_id"] = team["team_name"].map(country_map)
    team["federation_id"] = team["federation_name"].map(federation_map)
    team = team[
        [
            "team_id",
            "team_name",
            "team_code",
            "mens_team",
            "womens_team",
            "country_id",
            "federation_id",
            "confederation_id",
            "mens_team_wikipedia_link",
            "womens_team_wikipedia_link",
        ]
    ]
    team_name_to_id = dict(zip(team["team_name"], team["team_id"]))

    # ------------------------------------------------------------------
    # city y stadium
    # ------------------------------------------------------------------
    city_cols = ["city_name", "country_name", "city_wikipedia_link"]
    require_columns(stadiums, city_cols, "stadiums.csv")
    city = (
        stadiums[city_cols]
        .dropna(subset=["city_name", "country_name"])
        .drop_duplicates(subset=["city_name", "country_name"])
        .sort_values(["country_name", "city_name"])
        .reset_index(drop=True)
    )
    city["country_id"] = city["country_name"].map(country_map)
    city.insert(0, "city_id", range(1, len(city) + 1))
    city_lookup = {
        (row.city_name, row.country_name): row.city_id for row in city.itertuples()
    }
    city = city[["city_id", "city_name", "country_id", "city_wikipedia_link"]]

    stadium_cols = [
        "stadium_id",
        "stadium_name",
        "city_name",
        "country_name",
        "stadium_capacity",
        "stadium_wikipedia_link",
    ]
    require_columns(stadiums, stadium_cols, "stadiums.csv")
    stadium = stadiums[stadium_cols].drop_duplicates(subset=["stadium_id"]).copy()
    stadium["city_id"] = [
        city_lookup.get((c, k))
        for c, k in zip(stadium["city_name"], stadium["country_name"])
    ]
    stadium = stadium[
        [
            "stadium_id",
            "stadium_name",
            "city_id",
            "stadium_capacity",
            "stadium_wikipedia_link",
        ]
    ]

    # ------------------------------------------------------------------
    # position
    # ------------------------------------------------------------------
    position_frames = []
    for df in (squads, player_appearances):
        if {"position_code", "position_name"}.issubset(df.columns):
            position_frames.append(df[["position_code", "position_name"]])

    if not position_frames:
        raise ValueError("No se encontraron position_code y position_name en los CSV.")

    position = pd.concat(position_frames, ignore_index=True)
    position = (
        position.dropna(subset=["position_name"])
        .drop_duplicates(subset=["position_code", "position_name"])
        .sort_values(["position_name", "position_code"], na_position="last")
        .reset_index(drop=True)
    )
    position.insert(0, "position_id", range(1, len(position) + 1))

    # ------------------------------------------------------------------
    # tournament
    # ------------------------------------------------------------------
    tournament_cols = [
        "tournament_id",
        "tournament_name",
        "year",
        "start_date",
        "end_date",
        "host_country",
        "winner",
        "host_won",
        "count_teams",
        "group_stage",
        "second_group_stage",
        "final_round",
        "round_of_16",
        "quarter_finals",
        "semi_finals",
        "third_place_match",
        "final",
    ]
    require_columns(tournaments, tournament_cols, "tournaments.csv")
    tournament = tournaments[tournament_cols].drop_duplicates(subset=["tournament_id"]).copy()
    tournament["host_country_id"] = tournament["host_country"].map(country_map)
    tournament["winner_team_id"] = tournament["winner"].map(team_name_to_id)
    tournament = tournament[
        [
            "tournament_id",
            "tournament_name",
            "year",
            "start_date",
            "end_date",
            "host_country",
            "host_country_id",
            "winner",
            "winner_team_id",
            "host_won",
            "count_teams",
            "group_stage",
            "second_group_stage",
            "final_round",
            "round_of_16",
            "quarter_finals",
            "semi_finals",
            "third_place_match",
            "final",
        ]
    ]

    # ------------------------------------------------------------------
    # award y player
    # ------------------------------------------------------------------
    award_cols = ["award_id", "award_name", "award_description", "year_introduced"]
    require_columns(awards, award_cols, "awards.csv")
    award = awards[award_cols].drop_duplicates(subset=["award_id"])

    player_cols = [
        "player_id",
        "family_name",
        "given_name",
        "birth_date",
        "female",
        "goal_keeper",
        "defender",
        "midfielder",
        "forward",
        "count_tournaments",
        "list_tournaments",
        "player_wikipedia_link",
    ]
    require_columns(players, player_cols, "players.csv")
    player = players[player_cols].drop_duplicates(subset=["player_id"])

    # ------------------------------------------------------------------
    # matches
    # ------------------------------------------------------------------
    match_cols = [
        "match_id",
        "tournament_id",
        "match_name",
        "stage_name",
        "group_name",
        "group_stage",
        "knockout_stage",
        "replayed",
        "replay",
        "match_date",
        "match_time",
        "stadium_id",
        "home_team_id",
        "away_team_id",
        "score",
        "home_team_score",
        "away_team_score",
        "home_team_score_margin",
        "away_team_score_margin",
        "extra_time",
        "penalty_shootout",
        "score_penalties",
        "home_team_score_penalties",
        "away_team_score_penalties",
        "result",
        "home_team_win",
        "away_team_win",
        "draw",
    ]
    require_columns(matches, match_cols, "matches.csv")
    matches_clean = matches[match_cols].drop_duplicates(subset=["match_id"])

    # ------------------------------------------------------------------
    # player_appearance
    # ------------------------------------------------------------------
    pa_cols = [
        "tournament_id",
        "match_id",
        "team_id",
        "player_id",
        "position_code",
        "position_name",
        "home_team",
        "away_team",
        "shirt_number",
        "starter",
        "substitute",
    ]
    require_columns(player_appearances, pa_cols, "player_appearances.csv")
    player_appearance = player_appearances[pa_cols].copy()
    player_appearance = player_appearance.merge(
        position[["position_id", "position_code", "position_name"]],
        on=["position_code", "position_name"],
        how="left",
    )
    player_appearance = player_appearance[
        [
            "tournament_id",
            "match_id",
            "team_id",
            "player_id",
            "position_id",
            "home_team",
            "away_team",
            "shirt_number",
            "starter",
            "substitute",
        ]
    ].drop_duplicates(subset=["tournament_id", "match_id", "team_id", "player_id"])

    # ------------------------------------------------------------------
    # goal
    # ------------------------------------------------------------------
    goal_cols = [
        "goal_id",
        "tournament_id",
        "match_id",
        "team_id",
        "player_id",
        "player_team_id",
        "home_team",
        "away_team",
        "shirt_number",
        "minute_label",
        "minute_regulation",
        "minute_stoppage",
        "match_period",
        "own_goal",
        "penalty",
    ]
    require_columns(goals, goal_cols, "goals.csv")
    goal = goals[goal_cols].drop_duplicates(subset=["goal_id"])

    # ------------------------------------------------------------------
    # award_winner
    # ------------------------------------------------------------------
    aw_cols = ["tournament_id", "award_id", "player_id", "team_id", "shared"]
    require_columns(award_winners, aw_cols, "award_winners.csv")
    award_winner = award_winners[aw_cols].drop_duplicates(
        subset=["tournament_id", "award_id", "player_id"]
    )

    # Guardado en orden lógico
    save(confederation, "confederation")
    save(region, "region")
    save(country, "country")
    save(federation, "federation")
    save(team, "team")
    save(city, "city")
    save(stadium, "stadium")
    save(award, "award")
    save(player, "player")
    save(position, "position")
    save(tournament, "tournament")
    save(matches_clean, "matches")
    save(player_appearance, "player_appearance")
    save(goal, "goal")
    save(award_winner, "award_winner")

    print("\nPreparacion terminada. Los datos limpios estan en data/clean/.")


if __name__ == "__main__":
    main()
