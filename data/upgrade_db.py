import sqlite3
db=sqlite3.connect('data/mixart.db')
c=db.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
telegram_id INTEGER UNIQUE,
joined DATE DEFAULT CURRENT_DATE
)""")

c.execute("""CREATE TABLE IF NOT EXISTS payments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
order_id INTEGER,
method TEXT,
amount INTEGER,
status TEXT,
created DATE DEFAULT CURRENT_DATE
)""")

db.commit()
db.close()
print("✅ DB kengaytirildi")
