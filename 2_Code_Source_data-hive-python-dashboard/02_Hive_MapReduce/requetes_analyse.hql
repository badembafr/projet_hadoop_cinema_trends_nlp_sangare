-- 1. CREATION DES TABLES (SCHEMAS)

-- table movies : contient id, titre et genres
CREATE EXTERNAL TABLE IF NOT EXISTS movies (
    movieId INT,
    title STRING,
    genres STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/sangare/data/movies';

-- table ratings : contient les votes utilisateurs
CREATE EXTERNAL TABLE IF NOT EXISTS ratings (
    userId INT,
    movieId INT,
    rating FLOAT,
    timestamp BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/sangare/data/ratings';

-- table links : fait le lien entre movielens et tmdb
CREATE EXTERNAL TABLE IF NOT EXISTS links (
    movieId INT,
    imdbId STRING,
    tmdbId INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/sangare/data/links';

-- table tmdb_data : contient les descriptions et images recuperees via api
CREATE EXTERNAL TABLE IF NOT EXISTS tmdb_data (
    tmdb_id INT,
    description STRING,
    tmdb_url STRING,
    cover_url STRING,
    vote_average FLOAT,
    vote_count INT,
    original_language STRING,
    popularity FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/sangare/data/tmdb_enriched';


-- 2. REQUETES D'ANALYSE (RESULTATS POUR LE DASHBOARD)

-- kpi 1 : nombre total de films
INSERT OVERWRITE DIRECTORY '/user/sangare/output/kpi_movies'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT count(*) FROM movies;

-- kpi 2 : nombre de votes et note moyenne globale
INSERT OVERWRITE DIRECTORY '/user/sangare/output/kpi_ratings'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT count(*), avg(rating) FROM ratings;

-- analyse 1 : top 10 des meilleurs films (plus de 50 votes)
INSERT OVERWRITE DIRECTORY '/user/sangare/output/top10_films'
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
SELECT 
    m.title, 
    m.genres, 
    avg(r.rating) as avg_note, 
    count(r.rating) as nb_votes
FROM movies m
JOIN ratings r ON m.movieId = r.movieId
GROUP BY m.title, m.genres
HAVING nb_votes > 50
ORDER BY avg_note DESC
LIMIT 10;

-- analyse 2 : repartition des genres
INSERT OVERWRITE DIRECTORY '/user/sangare/output/genres_distribution'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT 
    single_genre, 
    count(*) as count
FROM movies 
LATERAL VIEW explode(split(genres, '\\|')) genreTable AS single_genre
GROUP BY single_genre
ORDER BY count DESC;

-- analyse 3 : top 10 des utilisateurs les plus actifs
INSERT OVERWRITE DIRECTORY '/user/sangare/output/top_users'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT 
    userId, 
    count(*) as nb_votes
FROM ratings
GROUP BY userId
ORDER BY nb_votes DESC
LIMIT 10;

-- analyse 4 : production de films par annee avec regex
INSERT OVERWRITE DIRECTORY '/user/sangare/output/evo_films_year'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT 
    regexp_extract(title, '.*\\(([0-9]{4})\\).*', 1) as year, 
    count(*) 
FROM movies 
WHERE regexp_extract(title, '.*\\(([0-9]{4})\\).*', 1) != ''
GROUP BY regexp_extract(title, '.*\\(([0-9]{4})\\).*', 1)
ORDER BY year;

-- analyse 5 : activite des votes par annee (conversion timestamp)
INSERT OVERWRITE DIRECTORY '/user/sangare/output/evo_votes_year'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT 
    from_unixtime(timestamp, 'yyyy') as year, 
    count(*) 
FROM ratings 
GROUP BY from_unixtime(timestamp, 'yyyy')
ORDER BY year;