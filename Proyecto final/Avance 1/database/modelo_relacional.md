# Modelo relacional - Avance 1

El siguiente diagrama resume las relaciones implementadas en database/schema.sql.

~~~mermaid
erDiagram
    REGION ||--o{ COUNTRY : contiene
    COUNTRY ||--o{ FEDERATION : posee
    CONFEDERATION ||--o{ FEDERATION : agrupa
    COUNTRY ||--o{ TEAM : representa
    FEDERATION ||--o{ TEAM : administra
    CONFEDERATION ||--o{ TEAM : agrupa

    COUNTRY ||--o{ CITY : contiene
    CITY ||--o{ STADIUM : contiene

    COUNTRY o|--o{ TOURNAMENT : anfitrion
    TEAM o|--o{ TOURNAMENT : ganador

    TOURNAMENT ||--o{ MATCHES : contiene
    STADIUM o|--o{ MATCHES : sede
    TEAM ||--o{ MATCHES : local
    TEAM ||--o{ MATCHES : visitante

    TOURNAMENT ||--o{ PLAYER_APPEARANCE : registra
    MATCHES ||--o{ PLAYER_APPEARANCE : registra
    TEAM ||--o{ PLAYER_APPEARANCE : alinea
    PLAYER ||--o{ PLAYER_APPEARANCE : participa
    POSITION o|--o{ PLAYER_APPEARANCE : posicion

    TOURNAMENT ||--o{ GOAL : registra
    MATCHES ||--o{ GOAL : contiene
    TEAM ||--o{ GOAL : anota
    PLAYER o|--o{ GOAL : marca

    TOURNAMENT ||--o{ AWARD_WINNER : entrega
    AWARD ||--o{ AWARD_WINNER : corresponde
    PLAYER ||--o{ AWARD_WINNER : recibe
    TEAM ||--o{ AWARD_WINNER : representa
~~~

## Claves primarias

| Tabla | Clave primaria |
|---|---|
| tournament | tournament_id |
| confederation | confederation_id |
| region | region_id |
| country | country_id |
| federation | federation_id |
| team | team_id |
| city | city_id |
| stadium | stadium_id |
| award | award_id |
| player | player_id |
| position | position_id |
| matches | match_id |
| player_appearance | tournament_id + match_id + team_id + player_id |
| goal | goal_id |
| award_winner | tournament_id + award_id + player_id |

## Criterios del diseno

Se conservaron como claves naturales los identificadores ya presentes en el conjunto de datos para torneos, confederaciones, equipos, estadios, jugadores, partidos, goles y premios.

Para las entidades que aparecen originalmente como texto repetido se generaron claves numericas:

- region_id
- country_id
- federation_id
- city_id
- position_id

Esto permite reducir redundancia y crear relaciones explicitas mediante claves foraneas.
