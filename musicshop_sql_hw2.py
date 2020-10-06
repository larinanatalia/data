import sqlalchemy
from pprint import pprint

db = 'postgresql://shopkeeper:*********@localhost:5432/musicshop'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

# 1 количество исполнителей в каждом жанре;
num_singergenre = connection.execute("""SELECT genrename, COUNT(idsinger) FROM singergenre s
JOIN genre g  ON s.idgenre = g.id
JOIN singer si ON s.idsinger = si.id
GROUP BY genrename
ORDER BY COUNT(idsinger) DESC;
""").fetchall()
pprint(num_singergenre)

# 2 количество треков, вошедших в альбомы 2019-2020 годов;
num_songs = connection.execute("""SELECT albumtitle, COUNT(songname) FROM song
JOIN album ON song.idalbum = album.id
WHERE album.year BETWEEN '2019-01-01' AND '2020-12-21'
GROUP BY albumtitle
ORDER BY COUNT(songname) DESC;
""").fetchall()
pprint(num_songs)

# 3 средняя продолжительность треков по каждому альбому;
avg_song_album = connection.execute("""SELECT albumtitle, AVG(duration) FROM song
JOIN album ON song.idalbum = album.id
GROUP BY albumtitle;
""").fetchall()
pprint(avg_song_album)

# 4 все исполнители, которые не выпустили альбомы в 2020 году;
singersalbum_before_2020 = connection.execute("""SELECT s.name FROM singeralbum sa
JOIN singer s ON sa.idsinger = s.id
JOIN album a ON sa.idalbum = a.id
WHERE a.year  NOT BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY s.name;
""").fetchall()
pprint(singersalbum_before_2020)

# 5 названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
collection_by_singer = connection.execute(""" SELECT c.name FROM singeralbum sa
JOIN singer s ON  sa.idsinger = s.id
JOIN album a ON sa.idalbum = a.id
JOIN song ON a.id = song.idalbum
JOIN collectionsong cs ON song.id = cs.idsong
JOIN collection c ON cs.idcollection = c.id
WHERE s.name LIKE '%%Лолита%%'
GROUP BY c.name
;
""").fetchall()
pprint(collection_by_singer)


# 6 название альбомов, в которых присутствуют исполнители более 1 жанра;
albums_with_morethen_1genre = connection.execute("""
SELECT albumtitle FROM (SELECT s.name, COUNT(sg.idgenre), a.albumtitle FROM singergenre sg
JOIN singer s ON sg.idsinger  = s.id
JOIN genre g ON sg.idgenre = g.id
JOIN singeralbum sa ON s.id = sa.idsinger
JOIN album a ON sa.idalbum = a.id
GROUP BY s.name, a.albumtitle) foo
WHERE count > 1
;
""").fetchall()
pprint(albums_with_morethen_1genre)

# 7 наименование треков, которые не входят в сборники;
songs_not_included_in_the_collection = connection.execute("""
SELECT s.songname FROM song s
LEFT JOIN collectionsong cs ON s.id = cs.idsong
WHERE cs.idsong IS NULL
;
""").fetchall()
pprint(songs_not_included_in_the_collection)

# 8 исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
shortest_track_by_singer = connection.execute ("""
SELECT name FROM (SELECT s.name, song.duration FROM singeralbum sa 
JOIN singer s ON  sa.idsinger = s.id
JOIN album a ON sa.idalbum = a.id 
JOIN song ON a.id = song.idalbum) g
WHERE duration = (SELECT MIN(duration) FROM (SELECT s.name, song.duration FROM singeralbum sa 
JOIN singer s ON  sa.idsinger = s.id
JOIN album a ON sa.idalbum = a.id 
JOIN song ON a.id = song.idalbum) foo)
;
""").fetchall()
pprint(shortest_track_by_singer)

# 9 название альбомов, содержащих наименьшее количество треков
min_songs_in_album = connection.execute("""
SELECT albumtitle  FROM (SELECT albumtitle, COUNT(songname) FROM album JOIN song ON album.id = song.idalbum GROUP BY albumtitle) foo
WHERE count = (SELECT MIN(count) FROM (SELECT albumtitle, COUNT(songname) FROM album JOIN song ON album.id = song.idalbum GROUP BY albumtitle) m)
;
""").fetchall()
pprint(min_songs_in_album)



