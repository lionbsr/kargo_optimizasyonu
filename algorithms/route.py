def create_route(stations):
    """
    stations: [(ilce_adi, mesafe_km), ...]
    Basit sezgisel: mesafeye göre sırala
    """
    sorted_route = sorted(stations, key=lambda x: x[1])
    return sorted_route
