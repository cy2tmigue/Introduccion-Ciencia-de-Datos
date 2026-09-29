from download_data import main as download_data
from prepare_data import main as prepare_data
from create_database import create_database_and_schema
from load_data import main as load_data


def main() -> None:
    print("=" * 70)
    print("AVANCE 1 - WORLD CUP DATABASE")
    print("=" * 70)

    print("\n1/4 Descargando CSV...")
    download_data()

    print("\n2/4 Limpiando y normalizando datos...")
    prepare_data()

    print("\n3/4 Creando base de datos y tablas...")
    create_database_and_schema()

    print("\n4/4 Cargando datos en MySQL...")
    load_data()

    print("\nProceso completo finalizado con exito.")


if __name__ == "__main__":
    main()
