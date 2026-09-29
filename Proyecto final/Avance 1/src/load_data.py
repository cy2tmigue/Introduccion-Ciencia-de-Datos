from pathlib import Path

import pandas as pd
import pymysql

from db_connection import get_database_connection, get_settings

PROJECT_DIR = Path(__file__).resolve().parents[1]
CLEAN_DIR = PROJECT_DIR / "data" / "clean"

TABLE_ORDER = [
    "confederation",
    "region",
    "country",
    "federation",
    "team",
    "city",
    "stadium",
    "award",
    "player",
    "position",
    "tournament",
    "matches",
    "player_appearance",
    "goal",
    "award_winner",
]


def load_table(connection, table: str, batch_size: int = 1000) -> int:
    path = CLEAN_DIR / f"{table}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero: python src/prepare_data.py"
        )

    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df = df.astype(object).replace(r"^\s*$", None, regex=True)

    columns = list(df.columns)
    quote = chr(96)
    column_sql = ", ".join(f"{quote}{column}{quote}" for column in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    sql = (
        f"INSERT INTO {quote}{table}{quote} ({column_sql}) "
        f"VALUES ({placeholders})"
    )

    total = 0
    with connection.cursor() as cursor:
        for start in range(0, len(df), batch_size):
            batch = df.iloc[start : start + batch_size]
            rows = [tuple(row) for row in batch.itertuples(index=False, name=None)]
            cursor.executemany(sql, rows)
            total += len(rows)

    return total


def main() -> None:
    settings = get_settings()
    print(
        f"Cargando datos en {settings['database']} "
        f"({settings['host']}:{settings['port']})...\n"
    )

    connection = get_database_connection()

    try:
        for table in TABLE_ORDER:
            count = load_table(connection, table)
            connection.commit()
            print(f"[OK] {table:18s} {count:>7} filas insertadas")

        print("\nCarga finalizada correctamente.")
    except (pymysql.MySQLError, FileNotFoundError, ValueError) as error:
        connection.rollback()
        print(f"\n[ERROR] La carga fue revertida: {error}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
