CREATE TABLE IF NOT EXISTS servers (
    server_id integer PRIMARY KEY,
    category_id integer,
    config_id integer,
    system_id integer,
    configured integer
);

CREATE TABLE IF NOT EXISTS games (
    game_id integer PRIMARY KEY,
    game_name text,
    server_id integer,
    category_id integer,
    system_id integer,
    resources_id integer,
    history_id integer,
    maps_id integer,
    p1_comms_id integer,
    p2_comms_id integer,
    p3_comms_id integer,
    p4_comms_id integer,
    gm_comms_id integer,
    party_voice_id integer,
    private_voice_id integer,
    gm_id integer,
    p1_id integer,
    p2_id integer,
    p3_id integer,
    p4_id integer
);

CREATE TABLE IF NOT EXISTS player_charaters (
    character_id integer PRIMARY KEY,
    game_id integer,
    player_id integer,
    icon blob,
    first_name text,
    last_name text,
    handle text,
    role text,
    role_ability text,
    role_ability_level integer,
    humanity integer,
    max_humanity integer
);

CREATE TABLE IF NOT EXISTS npcs (
    character_id integer PRIMARY KEY,
    game_id integer,
    icon blob,
    first_name text,
    last_name text,
    handle text,
    role text,
    role_ability text,
    role_ability_level integer,
    humanity integer,
    max_humanity integer
);