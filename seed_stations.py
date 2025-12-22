import sqlite3

stations = [
    ("İzmit",        40.766, 29.916),
    ("Başiskele",    40.715, 29.930),
    ("Çayırova",     40.824, 29.372),
    ("Darıca",       40.769, 29.379),
    ("Derince",      40.756, 29.830),
    ("Dilovası",     40.785, 29.543),
    ("Gebze",        40.770, 29.510),
    ("Gölcük",       40.716, 29.818),
    ("Kandıra",      41.070, 30.152),
    ("Karamürsel",   40.693, 29.616),
    ("Kartepe",      40.750, 29.960),
    ("Körfez",       40.767, 29.783)
]

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.executemany(
    "INSERT INTO stations (name, lat, lon) VALUES (?, ?, ?)",
    stations
)

conn.commit()
conn.close()

print("✅ Kocaeli ilçelerinin TAMAMI eklendi")
