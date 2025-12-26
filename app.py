from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import json

# Algoritmalar
from algorithms.optimizer import optimize_all_cargos


app = Flask(__name__)

# =====================================================
# VERİTABANI BAĞLANTISI
# =====================================================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# GİRİŞ / ROL SEÇİM SAYFASI
# =====================================================
@app.route("/")
def index():
    return render_template("index.html")


# =====================================================
# KULLANICI PANELİ
# =====================================================
@app.route("/user")
def user_panel():
    conn = get_db()
    stations = conn.execute("SELECT * FROM stations").fetchall()
    conn.close()
    return render_template("user.html", stations=stations)


# =====================================================
# KARGO EKLE (TEK + ÇOKLU DESTEK)
# =====================================================
@app.route("/add_cargo", methods=["POST"])
def add_cargo():

    cargos = request.get_json()

    if not cargos:
        return jsonify({"error": "Kargo verisi gelmedi"}), 400

    conn = get_db()

    for cargo in cargos:
        station_id = int(cargo["station_id"])
        weight = float(cargo["weight"])

        conn.execute(
            """
            INSERT INTO cargos (station_id, weight, date)
            VALUES (?, ?, DATE('now'))
            """,
            (station_id, weight)
        )

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


# =====================================================
# ADMIN PANELİ
# =====================================================
@app.route("/admin")
def admin_panel():
    conn = get_db()
    stations = conn.execute("SELECT * FROM stations").fetchall()
    conn.close()
    return render_template("admin.html", stations=stations)


# =====================================================
# TÜM KARGOLARI OPTİMİZE ET (ASİL HESAPLAMA BURADA)
# =====================================================
@app.route("/admin/optimize")
def admin_optimize():
    result = optimize_all_cargos()

    if result is None:
        return "⚠️ Henüz kargo yok."

    return render_template(
        "admin_result.html",
        result=result
    )


# =====================================================
# KULLANICI – KENDİ KARGOSUNUN SONUCU
# (KUŞ UÇUŞU YOK – SADECE ROTA GÖRÜNTÜLEME)
# =====================================================
@app.route("/user/result/<int:cargo_id>")
def user_result(cargo_id):
    conn = get_db()

    row = conn.execute("""
        SELECT
            cargos.id,
            cargos.station_id,
            cargos.weight,
            cargos.assigned_vehicle_id,
            stations.name,
            stations.lat,
            stations.lon
        FROM cargos
        JOIN stations ON cargos.station_id = stations.id
        WHERE cargos.id = ?
    """, (cargo_id,)).fetchone()

    conn.close()

    if row is None:
        return "⚠️ Kargo bulunamadı."

    return render_template(
        "result.html",
        station=row["name"],
        weight=row["weight"],
        vehicle=row["assigned_vehicle_id"],
        # 🔴 MESAFE & ROTA HESABI YOK
        # SADECE HARİTA GÖSTERİMİ
        start_lat=40.766,
        start_lon=29.916,
        dest_lat=row["lat"],
        dest_lon=row["lon"]
    )


# =====================================================
# İSTASYON EKLE (ADMIN)
# =====================================================
@app.route("/admin/add_station", methods=["POST"])
def add_station():
    name = request.form["name"].strip()
    lat = float(request.form["lat"])
    lon = float(request.form["lon"])

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO stations (name, lat, lon) VALUES (?, ?, ?)",
            (name, lat, lon)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "⚠️ Bu istasyon zaten mevcut."

    conn.close()
    return "✅ İstasyon başarıyla eklendi. <a href='/admin'>Geri dön</a>"


# =====================================================
# İSTASYONLARI API OLARAK VER (HARİTA İÇİN)
# =====================================================
@app.route("/stations")
def get_stations():
    conn = get_db()
    rows = conn.execute("SELECT * FROM stations").fetchall()
    conn.close()

    return jsonify([
        {
            "id": row["id"],
            "name": row["name"],
            "lat": row["lat"],
            "lon": row["lon"]
        }
        for row in rows
    ])

@app.route("/my_cargo/<int:cargo_id>")
def my_cargo(cargo_id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cargo = cur.execute("""
        SELECT
            cargos.id,
            cargos.weight,
            cargos.assigned_vehicle_id,
            stations.name AS station_name,
            stations.lat,
            stations.lon
        FROM cargos
        JOIN stations ON cargos.station_id = stations.id
        WHERE cargos.id = ?
    """, (cargo_id,)).fetchone()

    conn.close()

    if not cargo:
        return "Kargo bulunamadı"

    return render_template(
        "user_cargo.html",
        cargo=cargo
    )
@app.route("/user/cargos")
def user_cargos():
    conn = get_db()
    rows = conn.execute("""
        SELECT
            cargos.id,
            cargos.weight,
            cargos.assigned_vehicle_id,
            stations.name AS station_name,
            stations.lat,
            stations.lon
        FROM cargos
        JOIN stations ON cargos.station_id = stations.id
        ORDER BY cargos.id DESC
    """).fetchall()
    conn.close()

    return render_template("user_cargo.html", cargos=rows)

# =====================================================
# UYGULAMAYI BAŞLAT
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
