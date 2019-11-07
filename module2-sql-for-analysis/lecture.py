import psycopg2
import wget
print(dir(psycopg2))

help(psycopg2.connect)

dbname = 'yladesgz' #same as user
user = 'yladesgz' #same as dbname
pw = ''
host = 'salt.db.elephantsql.com' #from SERVER type this is a string

# Opening connector using details
pg_conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host)

# Create cursor using pg_conn
pg_curs = pg_conn.cursor()

# Execute command using cursor
pg_curs.execute('SELECT * FROM test_table;')

# You have to fetchall in a separate command when using postgreSQL to return the table
print(pg_curs.fetchall())

# Download file to follow lecture
#wget.download(url='https://github.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/blob/master/module1-introduction-to-sql/rpg_db.sqlite3?raw=true')

# Let's use some SQLite
import sqlite3

# Create connection and initiate cursor
sl_conn = sqlite3.connect('rpg_db.sqlite3')
sl_curs = sl_conn.cursor()

# Some queries
print(sl_curs.execute('SELECT COUNT(*) FROM charactercreator_character').fetchall())
print(sl_curs.execute('SELECT COUNT(DISTINCT name) FROM charactercreator_character').fetchall())

# Store query into variable
characters = sl_curs.execute('SELECT * FROM charactercreator_character').fetchall()
print(characters[0]) # Print first character
print(len(characters)) # Print number of characters

# Gives breakdown of table information
print(sl_curs.execute('PRAGMA table_info(charactercreator_character);').fetchall())

# Create table query, we'll use this on postgreSQL table
create_character_table = """
CREATE TABLE charactercreator_character (
character_id SERIAL PRIMARY KEY,
name VARCHAR(30),
level INT,
exp INT,
hp INT,
strength INT,
intelligence INT,
dexterity INT,
wisdom INT
);
"""

# Execute query from above to create table in postgreSQL
pg_curs.execute(create_character_table)

# Display tables from postgreSQL DB
show_tables = """
SELECT * FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog'
AND schemaname != 'information_schema';
"""

# Execute command from above
pg_curs.execute(show_tables)

# Print returned query
print(pg_curs.fetchall())

# We'll use this to insert characters into the table. We can leave out the index because it's auto generated
str(characters[0][1:])

# # Only inserts first character
# example_insert = """
# INSERT INTO charactercreator_character
# (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
# VALUES """ + str(characters[0][1:]) + ";"

# Insert every character into the postgreSQL DB
for character in characters:
    insert_character = """
        INSERT INTO charactercreator_character
        (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
        VALUES """ + str(character[1:]) + ";"
    pg_curs.execute(insert_character)

# Fetch the list of characters from the DB and store in new variable to test
pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_character = pg_curs.fetchall()

# Test each character is the same as the original list of characters
for character, pg_character in zip(characters, pg_character):
    assert character == pg_character

pg_curs.close()
pg_conn.commit()
