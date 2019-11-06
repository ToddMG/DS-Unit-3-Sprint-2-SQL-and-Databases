import sqlite3
import pandas as pd

df = pd.read_csv('buddymove_holidayiq.csv')
print(df)

conn = sqlite3.connect('buddymove_holidayiq.sqlite3')
df.to_sql('review', con=conn)

q1 = conn.execute('SELECT COUNT(*) FROM review').fetchone()
q2 = conn.execute('SELECT COUNT(*) FROM review WHERE Nature >= 100 AND Shopping >= 100').fetchall()
sports_avg = conn.execute('SELECT AVG(Sports) FROM review;').fetchone()
rel_avg = conn.execute('SELECT AVG(Religious) FROM review;').fetchone()
nat_avg = conn.execute('SELECT AVG(Nature) FROM review;').fetchone()
tht_avg = conn.execute('SELECT AVG(Theatre) FROM review;').fetchone()
shp_avg = conn.execute('SELECT AVG(Shopping) FROM review;').fetchone()
pic_avg = conn.execute('SELECT AVG(Picnic) FROM review;').fetchone()

q3 = {'Sports average':sports_avg, 'Religious Average':rel_avg, 'Nature Average':nat_avg,
        'Theatre Average':tht_avg, 'Shopping Average': shp_avg, 'Picnic Average':pic_avg}

print('Total number of rows:', q1)
print('Users who reviewed at least 100 in Nature and Shopping:', q2)
print(q3)

conn.close()

