import sqlite3
db=sqlite3.connect('data/mixart.db')
c=db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY, amount INTEGER, created DATE DEFAULT CURRENT_DATE)")
c.execute("CREATE TABLE IF NOT EXISTS admin(username TEXT, password TEXT)")
c.execute("INSERT OR IGNORE INTO admin VALUES('admin','admin123')")
db.commit()
db.close()
