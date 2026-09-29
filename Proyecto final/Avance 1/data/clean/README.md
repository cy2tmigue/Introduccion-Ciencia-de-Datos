# Datos limpios

Esta carpeta es generada por:

~~~bash
python src/prepare_data.py
~~~

El script usa Pandas para limpiar y normalizar los CSV de origen y genera exactamente los 15 archivos correspondientes a las tablas requeridas:

award, award_winner, city, confederation, country, federation, goal, matches, player, player_appearance, position, region, stadium, team y tournament.

Los archivos generados quedan listos para ser cargados a MySQL mediante:

~~~bash
python src/load_data.py
~~~
