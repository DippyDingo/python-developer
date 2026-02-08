
-- Жанры 
INSERT INTO genre (name) VALUES 
('Rock'),
('Pop'),
('Hip Hop'),
('Jazz'),
('Electronic');

-- Исполнители
INSERT INTO artist (name) VALUES 
('The Beatles'),
('Madonna'),
('Eminem'),
('Queen'),
('Taylor Swift'),
('Miles Davis');

-- Связи исполнителей с жанрами
INSERT INTO artist_genre (artist_id, genre_id) VALUES 
(1, 1), -- The Beatles - Rock
(1, 2), -- The Beatles - Pop
(2, 2), -- Madonna - Pop
(3, 3), -- Eminem - Hip Hop
(4, 1), -- Queen - Rock
(5, 2), -- Taylor Swift - Pop
(6, 4), -- Miles Davis - Jazz
(4, 2); -- Queen - Pop 

-- Альбомы 
INSERT INTO album (title, release_year) VALUES 
('Abbey Road', 1969),
('Like a Virgin', 1984),
('The Marshall Mathers LP', 2000),
('A Night at the Opera', 1975),
('1989', 2014),
('Kind of Blue', 1959),
('Future Nostalgia', 2020);

-- Связи исполнителей с альбомами
INSERT INTO artist_album (artist_id, album_id) VALUES 
(1, 1), -- The Beatles - Abbey Road
(2, 2), -- Madonna - Like a Virgin
(3, 3), -- Eminem - The Marshall Mathers LP
(4, 4), -- Queen - A Night at the Opera
(5, 5), -- Taylor Swift - 1989
(6, 6), -- Miles Davis - Kind of Blue
(2, 7); -- Madonna - Future Nostalgia

-- Треки 
INSERT INTO track (title, duration, album_id) VALUES 
('Come Together', 259, 1),
('Something', 183, 1),
('Like a Virgin', 211, 2),
('Material Girl', 244, 2),
('The Real Slim Shady', 284, 3),
('Stan', 404, 3),
('Bohemian Rhapsody', 354, 4),
('Love of My Life', 223, 4),
('Shake It Off', 219, 5),
('Blank Space', 231, 5),
('So What', 562, 6),
('Freddie Freeloader', 588, 6),
('Don''t Start Now', 183, 7),
('Physical', 194, 7),
('My Way', 276, 4), -- для задания 2 (содержит "my")
('Мой рай', 245, 2), -- для задания 2 (содержит "мой")
('Break My Soul', 240, 7);

-- Сборники 
INSERT INTO collection (title, release_year) VALUES 
('Best of 80s', 2018),
('Hip Hop Classics', 2019),
('Rock Legends', 2020),
('Pop Hits 2020', 2020),
('Jazz Masterpieces', 2021),
('Summer Hits', 2019),
('Golden Oldies', 2017);

-- Связи сборников с треками
INSERT INTO collection_track (collection_id, track_id) VALUES 
(1, 3),  -- Best of 80s - Like a Virgin
(1, 4),  -- Best of 80s - Material Girl
(2, 5),  -- Hip Hop Classics - The Real Slim Shady
(2, 6),  -- Hip Hop Classics - Stan
(3, 1),  -- Rock Legends - Come Together
(3, 7),  -- Rock Legends - Bohemian Rhapsody
(4, 9),  -- Pop Hits 2020 - Shake It Off
(4, 13), -- Pop Hits 2020 - Don't Start Now
(5, 11), -- Jazz Masterpieces - So What
(5, 12), -- Jazz Masterpieces - Freddie Freeloader
(6, 9),  -- Summer Hits - Shake It Off
(6, 13), -- Summer Hits - Don't Start Now
(7, 1),  -- Golden Oldies - Come Together
(7, 2),  -- Golden Oldies - Something
(4, 17), -- Pop Hits 2020 - Break My Soul
(3, 15); -- Rock Legends - My Way