import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("DELETE FROM stations")

conn.commit()
conn.close()

print("✅ stations tablosu temizlendi")
