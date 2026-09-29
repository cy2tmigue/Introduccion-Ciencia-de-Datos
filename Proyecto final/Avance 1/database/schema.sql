-- Avance 1 - Introduccion a Ciencia de Datos
-- Base de datos relacional para datos historicos de la Copa Mundial FIFA
-- Estudiante: Miguel Angel Quintero Puentes - 20252020029

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS award_winner;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS player_appearance;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS stadium;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS award;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS `position`;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS federation;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS confederation;
DROP TABLE IF EXISTS tournament;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE tournament (
    tournament_id VARCHAR(20) NOT NULL,
    tournament_name VARCHAR(150) NOT NULL,
    year SMALLINT,
    start_date DATE,
    end_date DATE,
    host_country VARCHAR(150),
    host_country_id INT NULL,
    winner VARCHAR(150),
    winner_team_id VARCHAR(20) NULL,
    host_won BOOLEAN,
    count_teams SMALLINT,
    group_stage BOOLEAN,
    second_group_stage BOOLEAN,
    final_round BOOLEAN,
    round_of_16 BOOLEAN,
    quarter_finals BOOLEAN,
    semi_finals BOOLEAN,
    third_place_match BOOLEAN,
    final BOOLEAN,
    PRIMARY KEY (tournament_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE confederation (
    confederation_id VARCHAR(20) NOT NULL,
    confederation_name VARCHAR(150) NOT NULL,
    confederation_code VARCHAR(20),
    confederation_wikipedia_link VARCHAR(500),
    PRIMARY KEY (confederation_id),
    UNIQUE KEY uq_confederation_code (confederation_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE region (
    region_id INT NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (region_id),
    UNIQUE KEY uq_region_name (region_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE country (
    country_id INT NOT NULL,
    country_name VARCHAR(120) NOT NULL,
    region_id INT NOT NULL,
    PRIMARY KEY (country_id),
    UNIQUE KEY uq_country_name (country_name),
    CONSTRAINT fk_country_region
        FOREIGN KEY (region_id) REFERENCES region(region_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE federation (
    federation_id INT NOT NULL,
    federation_name VARCHAR(180) NOT NULL,
    country_id INT NOT NULL,
    confederation_id VARCHAR(20) NOT NULL,
    federation_wikipedia_link VARCHAR(500),
    PRIMARY KEY (federation_id),
    UNIQUE KEY uq_federation_name (federation_name),
    CONSTRAINT fk_federation_country
        FOREIGN KEY (country_id) REFERENCES country(country_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_federation_confederation
        FOREIGN KEY (confederation_id) REFERENCES confederation(confederation_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE team (
    team_id VARCHAR(20) NOT NULL,
    team_name VARCHAR(120) NOT NULL,
    team_code VARCHAR(10),
    mens_team BOOLEAN,
    womens_team BOOLEAN,
    country_id INT NOT NULL,
    federation_id INT NOT NULL,
    confederation_id VARCHAR(20) NOT NULL,
    mens_team_wikipedia_link VARCHAR(500),
    womens_team_wikipedia_link VARCHAR(500),
    PRIMARY KEY (team_id),
    UNIQUE KEY uq_team_code (team_code),
    CONSTRAINT fk_team_country
        FOREIGN KEY (country_id) REFERENCES country(country_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_team_federation
        FOREIGN KEY (federation_id) REFERENCES federation(federation_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_team_confederation
        FOREIGN KEY (confederation_id) REFERENCES confederation(confederation_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE city (
    city_id INT NOT NULL,
    city_name VARCHAR(120) NOT NULL,
    country_id INT NOT NULL,
    city_wikipedia_link VARCHAR(500),
    PRIMARY KEY (city_id),
    UNIQUE KEY uq_city_country (city_name, country_id),
    CONSTRAINT fk_city_country
        FOREIGN KEY (country_id) REFERENCES country(country_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stadium (
    stadium_id VARCHAR(20) NOT NULL,
    stadium_name VARCHAR(180) NOT NULL,
    city_id INT NOT NULL,
    stadium_capacity INT,
    stadium_wikipedia_link VARCHAR(500),
    PRIMARY KEY (stadium_id),
    CONSTRAINT fk_stadium_city
        FOREIGN KEY (city_id) REFERENCES city(city_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE award (
    award_id VARCHAR(20) NOT NULL,
    award_name VARCHAR(120) NOT NULL,
    award_description VARCHAR(255),
    year_introduced SMALLINT,
    PRIMARY KEY (award_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE player (
    player_id VARCHAR(20) NOT NULL,
    family_name VARCHAR(120),
    given_name VARCHAR(120),
    birth_date DATE,
    female BOOLEAN,
    goal_keeper BOOLEAN,
    defender BOOLEAN,
    midfielder BOOLEAN,
    forward BOOLEAN,
    count_tournaments SMALLINT,
    list_tournaments TEXT,
    player_wikipedia_link VARCHAR(500),
    PRIMARY KEY (player_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `position` (
    position_id INT NOT NULL,
    position_code VARCHAR(20),
    position_name VARCHAR(80) NOT NULL,
    PRIMARY KEY (position_id),
    UNIQUE KEY uq_position_code (position_code),
    UNIQUE KEY uq_position_name (position_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE matches (
    match_id VARCHAR(30) NOT NULL,
    tournament_id VARCHAR(20) NOT NULL,
    match_name VARCHAR(180),
    stage_name VARCHAR(120),
    group_name VARCHAR(80),
    group_stage BOOLEAN,
    knockout_stage BOOLEAN,
    replayed BOOLEAN,
    replay BOOLEAN,
    match_date DATE,
    match_time VARCHAR(20),
    stadium_id VARCHAR(20) NULL,
    home_team_id VARCHAR(20) NOT NULL,
    away_team_id VARCHAR(20) NOT NULL,
    score VARCHAR(30),
    home_team_score SMALLINT,
    away_team_score SMALLINT,
    home_team_score_margin SMALLINT,
    away_team_score_margin SMALLINT,
    extra_time BOOLEAN,
    penalty_shootout BOOLEAN,
    score_penalties VARCHAR(30),
    home_team_score_penalties SMALLINT,
    away_team_score_penalties SMALLINT,
    result VARCHAR(80),
    home_team_win BOOLEAN,
    away_team_win BOOLEAN,
    draw BOOLEAN,
    PRIMARY KEY (match_id),
    CONSTRAINT fk_matches_tournament
        FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_matches_stadium
        FOREIGN KEY (stadium_id) REFERENCES stadium(stadium_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_matches_home_team
        FOREIGN KEY (home_team_id) REFERENCES team(team_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_matches_away_team
        FOREIGN KEY (away_team_id) REFERENCES team(team_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE player_appearance (
    tournament_id VARCHAR(20) NOT NULL,
    match_id VARCHAR(30) NOT NULL,
    team_id VARCHAR(20) NOT NULL,
    player_id VARCHAR(20) NOT NULL,
    position_id INT NULL,
    home_team BOOLEAN,
    away_team BOOLEAN,
    shirt_number SMALLINT,
    starter BOOLEAN,
    substitute BOOLEAN,
    PRIMARY KEY (tournament_id, match_id, team_id, player_id),
    CONSTRAINT fk_player_appearance_tournament
        FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_player_appearance_match
        FOREIGN KEY (match_id) REFERENCES matches(match_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_player_appearance_team
        FOREIGN KEY (team_id) REFERENCES team(team_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_player_appearance_player
        FOREIGN KEY (player_id) REFERENCES player(player_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_player_appearance_position
        FOREIGN KEY (position_id) REFERENCES `position`(position_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE goal (
    goal_id VARCHAR(30) NOT NULL,
    tournament_id VARCHAR(20) NOT NULL,
    match_id VARCHAR(30) NOT NULL,
    team_id VARCHAR(20) NOT NULL,
    player_id VARCHAR(20) NULL,
    player_team_id VARCHAR(20) NULL,
    home_team BOOLEAN,
    away_team BOOLEAN,
    shirt_number SMALLINT,
    minute_label VARCHAR(20),
    minute_regulation SMALLINT,
    minute_stoppage SMALLINT,
    match_period VARCHAR(50),
    own_goal BOOLEAN,
    penalty BOOLEAN,
    PRIMARY KEY (goal_id),
    CONSTRAINT fk_goal_tournament
        FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_goal_match
        FOREIGN KEY (match_id) REFERENCES matches(match_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_goal_team
        FOREIGN KEY (team_id) REFERENCES team(team_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_goal_player
        FOREIGN KEY (player_id) REFERENCES player(player_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_goal_player_team
        FOREIGN KEY (player_team_id) REFERENCES team(team_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE award_winner (
    tournament_id VARCHAR(20) NOT NULL,
    award_id VARCHAR(20) NOT NULL,
    player_id VARCHAR(20) NOT NULL,
    team_id VARCHAR(20) NOT NULL,
    shared BOOLEAN,
    PRIMARY KEY (tournament_id, award_id, player_id),
    CONSTRAINT fk_award_winner_tournament
        FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_award_winner_award
        FOREIGN KEY (award_id) REFERENCES award(award_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_award_winner_player
        FOREIGN KEY (player_id) REFERENCES player(player_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_award_winner_team
        FOREIGN KEY (team_id) REFERENCES team(team_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE tournament
    ADD CONSTRAINT fk_tournament_host_country
        FOREIGN KEY (host_country_id) REFERENCES country(country_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    ADD CONSTRAINT fk_tournament_winner_team
        FOREIGN KEY (winner_team_id) REFERENCES team(team_id)
        ON UPDATE CASCADE ON DELETE SET NULL;
