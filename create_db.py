import sqlite3

con = sqlite3.connect('calc.db')
cur = con.cursor()
with open("create_db.sql", "r", encoding="utf8") as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()