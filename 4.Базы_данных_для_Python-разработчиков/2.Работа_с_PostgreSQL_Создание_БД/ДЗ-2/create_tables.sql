CREATE table if NOT EXISTS genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Исполнители
CREATE TABLE artist (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE artist_genre (
    artist_id INTEGER NOT NULL REFERENCES artist(id),
    genre_id  INTEGER NOT NULL REFERENCES genre(id),
    PRIMARY KEY (artist_id, genre_id)      -- один артист может быть в нескольких жанрах
);

CREATE TABLE album (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,           -- название альбома
    release_year INTEGER                   -- год выпуска
);

CREATE TABLE artist_album (
    artist_id INTEGER NOT NULL REFERENCES artist(id),
    album_id  INTEGER NOT NULL REFERENCES album(id),
    PRIMARY KEY (artist_id, album_id)      -- у альбома несколько исполнителей и наоборот
);

CREATE TABLE track (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,           -- название трека
    duration INTEGER,                      -- длительность в секундах
    album_id INTEGER NOT NULL REFERENCES album(id)
);

CREATE TABLE collection (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,           -- название сборника
    release_year INTEGER                   -- год выпуска сборника
);

CREATE TABLE collection_track (
    collection_id INTEGER NOT NULL REFERENCES collection(id),
    track_id      INTEGER NOT NULL REFERENCES track(id),
    PRIMARY KEY (collection_id, track_id)  -- трек может быть в нескольких сборниках
);