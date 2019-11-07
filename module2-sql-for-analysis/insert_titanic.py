import psycopg2

dbname = 'yladesgz'  # same as user
user = 'yladesgz'  # same as dbname
pw = ''
host = 'salt.db.elephantsql.com'  # from SERVER type this is a string

# Initiate connector to ElephantSQL
pg_conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host)

# Initiate cursor
pg_curs = pg_conn.cursor()

# Create enumerated type
pg_curs.execute("CREATE TYPE sex AS ENUM ('male', 'female');")

# Create elephantSQL table
pg_curs.execute("""
CREATE TABLE titanic (
survived boolean,
class INT,
name VARCHAR(100) NOT NULL,
sex SEX,
age FLOAT,
sib_spouse INT,
par_child INT,
fare FLOAT
);""")

# We could create a SQLite3 file using a pandas DF and then converting that to a postgreSQL table,
# but that's far too convoluted for a function psycopg2 already has.

# Open the csv file as f, and insert it into the 'titanic' table.
with open('titanic.csv', 'r') as f:
    next(f)  # Skip the header row.
    pg_curs.copy_from(f, 'titanic', sep=',')

pg_conn.commit()  # Commit changes.
pg_curs.close()  # Close cursor.
pg_conn.close()  # Close connector.
