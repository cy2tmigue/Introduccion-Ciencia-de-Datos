from pathlib import Path
import requests

BASE_URL = "https://raw.githubusercontent.com/jfjelstul/worldcup/master/data-csv"

FILES = [
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

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"


def download_file(filename: str, overwrite: bool = False) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destination = RAW_DIR / filename

    if destination.exists() and not overwrite:
        print(f"[OMITIDO] {filename} ya existe")
        return

    url = f"{BASE_URL}/{filename}"
    print(f"[DESCARGANDO] {filename}")

    response = requests.get(url, timeout=120)
    response.raise_for_status()
    destination.write_bytes(response.content)

    print(f"[OK] {filename} -> {destination}")


def main() -> None:
    print("Descarga de archivos CSV - Fjelstul World Cup Database")
    print(f"Destino: {RAW_DIR}")

    for filename in FILES:
        download_file(filename)

    print("\nDescarga finalizada correctamente.")


if __name__ == "__main__":
    main()
