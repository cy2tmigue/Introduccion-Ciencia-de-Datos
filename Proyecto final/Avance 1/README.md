# Avance 1 - Base de datos de Mundiales FIFA

**Integrante:** Miguel Angel Quintero Puentes  
**Codigo:** 20252020029

## Descripcion

Este avance construye la base relacional del proyecto de Introduccion a Ciencia de Datos utilizando informacion historica de la Copa Mundial FIFA.

El objetivo de esta entrega es:

- organizar la informacion en una base de datos relacional;
- definir claves primarias y foraneas;
- mantener integridad referencial;
- leer los archivos CSV con Pandas;
- limpiar y normalizar los datos;
- cargar automaticamente la informacion a MySQL;
- mostrar mensajes de exito o error durante la carga.

No se incluye dashboard, Machine Learning ni desarrollo web porque no forman parte del alcance del Avance 1.

## Integrante

| Nombre | Codigo |
|---|---|
| Miguel Angel Quintero Puentes | 20252020029 |

## Tecnologias

- Python 3.10+
- Pandas
- MySQL / MariaDB
- XAMPP
- PyMySQL
- Requests
- python-dotenv
- Git y GitHub

## Fuente de datos

Los datos se obtienen del proyecto **Fjelstul World Cup Database**:

- Repositorio: https://github.com/jfjelstul/worldcup
- Autor: Joshua C. Fjelstul, Ph.D.
- Copyright: © 2023 Joshua C. Fjelstul, Ph.D.
- Licencia indicada por el repositorio fuente: CC-BY-SA 4.0

Para este avance se utilizan 11 CSV de la carpeta data-csv y se normalizan para construir las 15 tablas solicitadas.

### Transformaciones realizadas

Los CSV originales contienen algunos atributos repetidos para facilitar el analisis. En este proyecto se transforman a un modelo mas relacional:

- se crean tablas independientes para region, country, federation, city y position;
- se generan identificadores numericos para esas entidades;
- se reemplazan datos repetidos por claves foraneas;
- se eliminan duplicados en tablas maestras;
- se conservan los identificadores originales de torneos, equipos, jugadores, estadios, partidos, goles y premios;
- los datos originales descargados no se sobrescriben.

Como referencia de las herramientas usadas durante el curso tambien se reviso:
https://github.com/daniloperama2006/IoD_ACM

Ese repositorio se utilizo solamente como referencia del entorno Python + MySQL/XAMPP. Este avance no incluye Streamlit.

## Tablas implementadas

El modelo contiene exactamente las 15 tablas requeridas:

1. award
2. award_winner
3. city
4. confederation
5. country
6. federation
7. goal
8. matches
9. player
10. player_appearance
11. position
12. region
13. stadium
14. team
15. tournament

El archivo principal del modelo es database/schema.sql.

El detalle de las relaciones se encuentra en database/modelo_relacional.md.

## Estructura del proyecto

~~~text
Avance 1/
|
|-- database/
|   |-- schema.sql
|   +-- modelo_relacional.md
|
|-- data/
|   |-- raw/
|   |   +-- README.md
|   +-- clean/
|       +-- README.md
|
|-- src/
|   |-- db_connection.py
|   |-- download_data.py
|   |-- prepare_data.py
|   |-- create_database.py
|   |-- load_data.py
|   +-- run_all.py
|
|-- .env.example
|-- .gitignore
|-- requirements.txt
+-- README.md
~~~

## Preparacion del entorno

### 1. Entrar a la carpeta del avance

En PowerShell:

~~~powershell
cd "Proyecto final\Avance 1"
~~~

### 2. Crear un entorno virtual

~~~powershell
python -m venv .venv
~~~

Activarlo:

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

### 3. Instalar dependencias

~~~powershell
python -m pip install -r requirements.txt
~~~

## Configuracion de MySQL

Inicia MySQL desde XAMPP.

Copia el archivo de ejemplo:

~~~powershell
Copy-Item .env.example .env
~~~

Edita .env segun tu instalacion.

Configuracion tipica de XAMPP:

~~~text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=world_cup
~~~

Si en XAMPP MySQL esta configurado en el puerto 4040, cambia solamente:

~~~text
MYSQL_PORT=4040
~~~

No se deben subir contrasenas reales al repositorio. El archivo .env esta excluido por .gitignore.

## Ejecucion automatica

Con MySQL iniciado, el proyecto completo se puede ejecutar con un solo comando:

~~~powershell
python src/run_all.py
~~~

Ese comando realiza cuatro pasos:

1. descarga los CSV fuente;
2. limpia y normaliza los datos con Pandas;
3. crea la base de datos world_cup y las 15 tablas;
4. inserta los datos en MySQL respetando el orden de las claves foraneas.

Al finalizar se muestran mensajes de exito por cada tabla.

## Ejecucion paso a paso

### Descargar los CSV

~~~powershell
python src/download_data.py
~~~

### Limpiar y normalizar

~~~powershell
python src/prepare_data.py
~~~

Los CSV limpios quedan en data/clean/.

### Crear la base de datos y las tablas

~~~powershell
python src/create_database.py
~~~

### Cargar los datos

~~~powershell
python src/load_data.py
~~~

La salida muestra la cantidad de filas insertadas por tabla y un mensaje final de carga exitosa.

## Integridad referencial

El esquema utiliza InnoDB y claves foraneas. Algunas relaciones principales son:

- country a region
- federation a country y confederation
- team a country, federation y confederation
- city a country
- stadium a city
- matches a tournament, stadium y team
- player_appearance a tournament, matches, team, player y position
- goal a tournament, matches, team y player
- award_winner a tournament, award, player y team
- tournament a country anfitrion y team ganador cuando existe coincidencia directa

## Archivos CSV limpios

prepare_data.py genera:

~~~text
award.csv
award_winner.csv
city.csv
confederation.csv
country.csv
federation.csv
goal.csv
matches.csv
player.csv
player_appearance.csv
position.csv
region.csv
stadium.csv
team.csv
tournament.csv
~~~

## Notas

- La base de datos se puede recrear cuantas veces sea necesario.
- Los datos originales se guardan en data/raw y los normalizados en data/clean.
- Las credenciales de MySQL se configuran mediante variables de entorno.
- No se implementan procedimientos almacenados ni vistas porque no son requeridos en esta entrega.
