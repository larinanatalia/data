import sqlalchemy

db = 'postgresql://shopkeeper:*******@localhost:5432/musicshop'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

albums2018 = connection.execute("""SELECT albumtitle, year FROM album WHERE year BETWEEN '2018-01-01' AND '2018-12-21';
""").fetchall()
print(albums2018)

longest_song = connection.execute("""SELECT songname, duration FROM song ORDER BY duration DESC;
""").fetchone()
print(longest_song)

more_long_than = connection.execute("""SELECT songname FROM song WHERE duration >= 210;
""").fetchall()
print(more_long_than)

collections = connection.execute("""SELECT name FROM collection WHERE year BETWEEN '2018-01-01' AND '2020-12-21;'
""").fetchall()
print(collections)

singer_name = connection.execute("""SELECT name FROM singer WHERE name NOT LIKE '%% %%';
""").fetchall()
print(singer_name)

word_en = connection.execute("""SELECT songname FROM song WHERE songname LIKE '%%My%%';
""").fetchall()
word_ru = connection.execute("""SELECT songname FROM song WHERE songname LIKE '%%Мой%%';
""").fetchall()

print(word_en)
print(word_ru)






