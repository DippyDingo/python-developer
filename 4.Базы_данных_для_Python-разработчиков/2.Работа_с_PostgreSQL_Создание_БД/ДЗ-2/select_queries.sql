
-- Задание 2
-- 1. Название и продолжительность самого длинного трека
SELECT title, duration 
FROM track 
WHERE duration = (SELECT MAX(duration) FROM track);

-- 2. Название треков, продолжительность которых не менее 3,5 минут (210 секунд)
SELECT title, duration 
FROM track 
WHERE duration >= 210 
ORDER BY duration DESC;

-- 3. Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT title, release_year 
FROM collection 
WHERE release_year BETWEEN 2018 AND 2020 
ORDER BY release_year;

-- 4. Исполнители, чьё имя состоит из одного слова
SELECT name 
FROM artist 
WHERE name NOT LIKE '% %' AND name NOT LIKE '%-%';

-- 5. Название треков, которые содержат слово «мой» или «my»
SELECT title 
FROM track 
WHERE LOWER(title) LIKE '%мой%' OR LOWER(title) LIKE '%my%';

-- Задание 3
-- 1. Количество исполнителей в каждом жанре
SELECT g.name AS genre_name, COUNT(ag.artist_id) AS artist_count
FROM genre g
LEFT JOIN artist_genre ag ON g.id = ag.genre_id
GROUP BY g.id, g.name
ORDER BY artist_count DESC;

-- 2. Количество треков, вошедших в альбомы 2019–2020 годов
SELECT COUNT(t.id) AS track_count
FROM track t
JOIN album a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

-- 3. Средняя продолжительность треков по каждому альбому
SELECT a.title AS album_title, 
       ROUND(AVG(t.duration), 2) AS avg_duration_seconds,
       ROUND(AVG(t.duration)/60, 2) AS avg_duration_minutes
FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY a.id, a.title
ORDER BY avg_duration_seconds DESC;

-- 4. Все исполнители, которые не выпустили альбомы в 2020 году
SELECT DISTINCT ar.name AS artist_name
FROM artist ar
WHERE ar.id NOT IN (
    SELECT aa.artist_id
    FROM artist_album aa
    JOIN album al ON aa.album_id = al.id
    WHERE al.release_year = 2020
)
ORDER BY ar.name;

-- 5. Названия сборников, в которых присутствует конкретный исполнитель 
SELECT DISTINCT c.title AS collection_title, c.release_year
FROM collection c
JOIN collection_track ct ON c.id = ct.collection_id
JOIN track t ON ct.track_id = t.id
JOIN album a ON t.album_id = a.id
JOIN artist_album aa ON a.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE ar.name = 'Madonna'
ORDER BY c.release_year DESC;

-- Задание 4 
-- 1. Названия альбомов, в которых присутствуют исполнители более чем одного жанра
SELECT DISTINCT a.title AS album_title
FROM album a
JOIN artist_album aa ON a.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE ar.id IN (
    SELECT artist_id
    FROM artist_genre
    GROUP BY artist_id
    HAVING COUNT(genre_id) > 1
)
ORDER BY a.title;

-- 2. Наименования треков, которые не входят в сборники
SELECT t.title AS track_title, a.title AS album_title
FROM track t
JOIN album a ON t.album_id = a.id
WHERE t.id NOT IN (
    SELECT track_id
    FROM collection_track
)
ORDER BY t.title;

-- 3. Исполнитель или исполнители, написавшие самый короткий по продолжительности трек
SELECT ar.name AS artist_name, t.title AS track_title, t.duration
FROM artist ar
JOIN artist_album aa ON ar.id = aa.artist_id
JOIN album a ON aa.album_id = a.id
JOIN track t ON a.id = t.album_id
WHERE t.duration = (SELECT MIN(duration) FROM track)
ORDER BY ar.name;

-- 4. Названия альбомов, содержащих наименьшее количество треков
SELECT a.title AS album_title, COUNT(t.id) AS track_count
FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY a.id, a.title
HAVING COUNT(t.id) = (
    SELECT COUNT(t2.id) as cnt
    FROM album a2
    JOIN track t2 ON a2.id = t2.album_id
    GROUP BY a2.id
    ORDER BY cnt
    LIMIT 1
)
ORDER BY a.title;

SELECT a.title, COUNT(t.id) as track_count
FROM album a
LEFT JOIN track t ON a.id = t.album_id
GROUP BY a.id, a.title
ORDER BY track_count;

-- Проверка жанров исполнителей
SELECT ar.name AS artist_name, 
       STRING_AGG(g.name, ', ') AS genres,
       COUNT(g.id) AS genre_count
FROM artist ar
JOIN artist_genre ag ON ar.id = ag.artist_id
JOIN genre g ON ag.genre_id = g.id
GROUP BY ar.id, ar.name
HAVING COUNT(g.id) > 1
ORDER BY genre_count DESC;