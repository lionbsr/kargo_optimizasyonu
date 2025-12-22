# algorithms/optimizer.py
import sqlite3
from math import radians, sin, cos, sqrt, atan2

from algorithms.graph import greedy_route
from algorithms.vehicle import Vehicle


# -------------------------------------------------
# Haversine (kuş uçuşu – SADECE HESAPLAMA)
# -------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# -------------------------------------------------
# ANA OPTİMİZASYON
# -------------------------------------------------
def optimize_all_cargos():
    start = {
        "name": "İzmit",
        "lat": 40.766,
        "lon": 29.916,
        "weight": 0   # 🔴 KRİTİK: tablo & jinja için
    }

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # -------------------------------------------------
    # 1️⃣ YARIN DAĞITILACAK KARGOLAR (İSTASYON BAZLI)
    # -------------------------------------------------
    stations = cur.execute("""
        SELECT
            stations.id AS station_id,
            stations.name,
            stations.lat,
            stations.lon,
            SUM(cargos.weight) AS total_weight
        FROM cargos
        JOIN stations ON cargos.station_id = stations.id
        WHERE cargos.date = DATE('now', '+1 day')
        GROUP BY stations.id
    """).fetchall()

    if not stations:
        conn.close()
        return None

    station_nodes = [
        {
            "station_id": s["station_id"],
            "name": s["name"],
            "lat": s["lat"],
            "lon": s["lon"],
            "total_weight": s["total_weight"]
        }
        for s in stations
    ]

    # -------------------------------------------------
    # 2️⃣ GREEDY → GLOBAL ZİYARET SIRASI
    # -------------------------------------------------
    route = greedy_route(start, station_nodes)

    # -------------------------------------------------
    # 3️⃣ TOPLAM KUŞ UÇUŞU MESAFE (GLOBAL)
    # -------------------------------------------------
    total_distance = 0
    prev = start
    for step in route:
        total_distance += haversine(
            prev["lat"], prev["lon"],
            step["lat"], step["lon"]
        )
        prev = step

    total_weight = sum(s["total_weight"] for s in station_nodes)

    # -------------------------------------------------
    # 4️⃣ ÇOKLU ARAÇ MODELİ (BIN PACKING – GREEDY)
    # -------------------------------------------------
    vehicles = [
        Vehicle(vehicle_id=1, capacity=500),
        Vehicle(vehicle_id=2, capacity=750),
        Vehicle(vehicle_id=3, capacity=1000)
    ]

    rental_vehicle = Vehicle(
        vehicle_id=99,
        capacity=10**9,
        rent_cost=200
    )

    station_nodes_sorted = sorted(
        station_nodes,
        key=lambda x: x["total_weight"],
        reverse=True
    )

    for station in station_nodes_sorted:
        placed = False

        for vehicle in vehicles:
            if vehicle.remaining_capacity >= station["total_weight"]:
                vehicle.remaining_capacity -= station["total_weight"]
                vehicle.stations.add(station["station_id"])
                placed = True

                cur.execute("""
                    UPDATE cargos
                    SET assigned_vehicle_id = ?
                    WHERE station_id = ?
                    AND date = DATE('now', '+1 day')
                """, (vehicle.id, station["station_id"]))
                break

        if not placed:
            rental_vehicle.remaining_capacity -= station["total_weight"]
            rental_vehicle.stations.add(station["station_id"])

            cur.execute("""
                UPDATE cargos
                SET assigned_vehicle_id = ?
                WHERE station_id = ?
                AND date = DATE('now', '+1 day')
            """, (rental_vehicle.id, station["station_id"]))

    if rental_vehicle.stations:
        vehicles.append(rental_vehicle)

    conn.commit()

    # -------------------------------------------------
    # 5️⃣ ARAÇ BAZLI ROTA + MESAFE + MALİYET
    # -------------------------------------------------
    vehicle_routes = []

    for vehicle in vehicles:
        if not vehicle.stations:
            continue

        rows = cur.execute("""
            SELECT
                stations.id,
                stations.name,
                stations.lat,
                stations.lon,
                SUM(cargos.weight) AS total_weight
            FROM cargos
            JOIN stations ON cargos.station_id = stations.id
            WHERE cargos.assigned_vehicle_id = ?
            GROUP BY stations.id
        """, (vehicle.id,)).fetchall()

        # 🔴 GREEDY SIRAYA GÖRE DÜZENLE
        ordered = [
            r for step in route
            for r in rows
            if r["id"] == step["station_id"]
        ]

        # 🔴 BAŞLANGIÇ + ROTA (İzmit weight=0)
        full_route = [start] + [
            {
                "name": r["name"],
                "lat": r["lat"],
                "lon": r["lon"],
                "weight": r["total_weight"]
            }
            for r in ordered
        ]

        # 🔴 ARAÇ MESAFESİ (KUŞ UÇUŞU – HESAPLAMA)
        vehicle_distance = 0
        for i in range(len(full_route) - 1):
            vehicle_distance += haversine(
                full_route[i]["lat"], full_route[i]["lon"],
                full_route[i + 1]["lat"], full_route[i + 1]["lon"]
            )

        # 🔴 ARAÇ MALİYETİ
        travel_cost = vehicle_distance * 1.2
        vehicle_cost = travel_cost + vehicle.rent_cost

        vehicle_routes.append({
            "vehicle_id": vehicle.id,
            "rent_cost": vehicle.rent_cost,
            "distance": round(vehicle_distance, 2),
            "cost": round(vehicle_cost, 2),
            "stations": full_route
        })

    conn.close()

    # -------------------------------------------------
    # 6️⃣ DÖNÜŞ
    # -------------------------------------------------
    return {
        "start": start,
        "route": route,
        "vehicle_routes": vehicle_routes,
        "total_weight": total_weight,
        "total_distance": round(total_distance, 2),
        "total_cost": round(sum(v["cost"] for v in vehicle_routes), 2)
    }
