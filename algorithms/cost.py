def calculate_cost(route):
    """
    route: [(ilce_adi, mesafe_km)]
    Yol maliyeti: 1 km = 1 birim
    """
    total_distance = sum([r[1] for r in route])
    total_cost = total_distance * 1
    return total_cost
