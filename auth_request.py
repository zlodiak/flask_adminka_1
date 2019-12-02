import psycopg2

db_conn = psycopg2.connect(
    database='flask_adminka', 
    user='flask_admin', 
    password='flask_admin',        
    host='localhost'
)
db_cursor = db_conn.cursor()

db_cursor.execute("select * from users")
records = db_cursor.fetchall() 
for row in records:
   print("Id = ", row[0], )
   print("pass = ", row[1])
   print("email  = ", row[2], "\n")
   print("active  = ", row[3], "\n")