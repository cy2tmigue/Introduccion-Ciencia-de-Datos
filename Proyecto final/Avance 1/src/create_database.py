import re
from pathlib import Path

import pymysql

from db_connection import get_database_connection, get_server_connection, get_settings

PROJECT_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_DIR / "database" / "schema.sql"


def validate_database_name(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", name):
        raise ValueError("MYSQL_DATABASE solo puede contener letras, numeros y guion bajo.")
    return name


def split_sql_statements(sql: str) -> list[str]:
    statements = []
    current = []

    for line in sql.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue

        current.append(line)

        if stripped.endswith(";"):
            statement = "\n".join(current).strip()
            statements.append(statement[:-1].strip())
            current = []

    if current:
        statements.append("\n".join(current).strip())

    return [statement for statement in statements if statement]


def create_database_and_schema() -> None:
    settings = get_settings()
    database = validate_database_name(settings["database"])

    print(
        f"Conectando a MySQL en {settings['host']}:{settings['port']} "
        f"como {settings['user']}..."
    )

    with get_server_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {database} "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )

    print(f"[OK] Base de datos disponible: {database}")

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"No se encontro el esquema SQL: {SCHEMA_PATH}")

    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    statements = split_sql_statements(sql)

    connection = get_database_connection()
    try:
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
        connection.commit()
        print(f"[OK] Esquema creado correctamente ({len(statements)} sentencias).")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main() -> None:
    try:
        create_database_and_schema()
    except pymysql.MySQLError as error:
        print(f"[ERROR MYSQL] {error}")
        raise


if __name__ == "__main__":
    main()
