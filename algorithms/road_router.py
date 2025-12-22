from .roads import ROAD_GRAPH


def build_road_route(order):
    """
    order: ["İzmit", "Derince", "Gölcük", ...]
    dönüş: [(lat, lon), (lat, lon), ...]  → haritada çizilecek noktalar
    """

    points = []

    # Tek nokta varsa yol çizilmez
    if not order or len(order) < 2:
        return points

    for i in range(len(order) - 1):
        a = order[i]
        b = order[i + 1]

        # 🔒 Aynı noktaysa atla (İzmit -> İzmit gibi)
        if a == b:
            continue

        # 🔒 Yol tanımlı mı kontrol et
        if a not in ROAD_GRAPH or b not in ROAD_GRAPH[a]:
            print(f"⚠️ Karayolu tanımlı değil: {a} -> {b} (atlanıyor)")
            continue   # ❗ exception atma, sistemi düşürme

        segment = ROAD_GRAPH[a][b]

        # 🔹 İlk segment tam eklenir
        if not points:
            points.extend(segment)
        else:
            # 🔹 İlk nokta tekrar etmesin
            points.extend(segment[1:])

    return points
