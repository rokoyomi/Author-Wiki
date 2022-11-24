import mysql.connector

conn = mysql.connector.connect(
    user="sarim",password="12345678",database='db_database'
)

cur = conn.cursor(dictionary=True)
cur.execute('select * from author where id = 5')
print(cur.fetchone())