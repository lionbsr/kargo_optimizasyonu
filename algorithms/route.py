def create_route(stations):
    """
    stations: [(district_name, distance_km), ...]

    Kullanılan yöntem:
    Greedy (Açgözlü) Yaklaşım

    Mantık:
    - En yakın noktadan başlanır
    - Mesafeye göre sıralama yapılır
    """

    if not stations:
        return []

    # Mesafeye göre artan sırala
    route = sorted(stations, key=lambda x: x[1])

    return route
