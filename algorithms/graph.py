from math import radians, sin, cos, sqrt, atan2

# -------------------------------
# KOCAELİ KARA YOLU GRAFI
# -------------------------------
ROAD_GRAPH = {
    "İzmit": ["Derince", "Kartepe", "Başiskele", "Körfez", "Kandıra"],
    "Derince": ["İzmit", "Körfez"],
    "Körfez": ["Derince", "İzmit", "Dilovası"],
    "Dilovası": ["Körfez", "Gebze"],
    "Gebze": ["Dilovası", "Darıca", "Çayırova"],
    "Darıca": ["Gebze"],
    "Çayırova": ["Gebze"],
    "Başiskele": ["İzmit", "Gölcük"],
    "Gölcük": ["Başiskele", "Karamürsel"],
    "Karamürsel": ["Gölcük"],
    "Kartepe": ["İzmit"],
    "Kandıra": ["İzmit"]
}

# -------------------------------
# HAVERSINE MESAFE
# -------------------------------
def distance(a, b):
    R = 6371
    dlat = radians(b["lat"] - a["lat"])
    dlon = radians(b["lon"] - a["lon"])
    lat1 = radians(a["lat"])
    lat2 = radians(b["lat"])

    x = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(x), sqrt(1 - x))
    return R * c


# -------------------------------
# GREEDY + GRAF TABANLI ROTA
# -------------------------------
def greedy_route(start, stations):
    route = []
    current = start
    remaining = stations.copy()

def greedy_route(start, stations):
    route = []
    current = start
    remaining = stations.copy()

    while remaining:
        nearest = min(
            remaining,
            key=lambda s: distance(current, s)
        )
        d = distance(current, nearest)
        route.append(nearest)   # 🔴 sadece name değil, node
        current = nearest
        remaining.remove(nearest)

    return route

