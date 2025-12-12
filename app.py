from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# -----------------------------
# Veritabanı bağlantısı
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# Kullanıcı Paneli
# -----------------------------
@app.route("/")
def user_panel():
    return render_template("user.html")

# -----------------------------
# Admin Paneli
# -----------------------------
@app.route("/admin")
def admin_panel():
    return render_template("admin.html")

# -----------------------------
# Uygulama başlatma
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
