create table genre (
	id SERIAL PRIMARY KEY,
	name varchar(100) not null
);

create table artist (
	id SERIAL primary key,
	name varchar(100) not null
);

CREATE TABLE artist_genre (
    artist_id INTEGER NOT NULL REFERENCES artist(id),
    genre_id  INTEGER NOT NULL REFERENCES genre(id),
    PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE album (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    release_year INTEGER
);

CREATE TABLE artist_album (
    artist_id INTEGER NOT NULL REFERENCES artist(id),
    album_id  INTEGER NOT NULL REFERENCES album(id),
    PRIMARY KEY (artist_id, album_id)
);

CREATE TABLE track (
    id       SERIAL PRIMARY KEY,
    title    VARCHAR(200) NOT NULL,
    duration INTEGER,
    album_id INTEGER NOT NULL REFERENCES album(id)
);

CREATE TABLE collection (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    release_year INTEGER
);

CREATE TABLE collection_track (
    collection_id INTEGER NOT NULL REFERENCES collection(id),
    track_id      INTEGER NOT NULL REFERENCES track(id),
    PRIMARY KEY (collection_id, track_id)
);