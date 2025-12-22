def calculate_cost(distance_km, weight_kg, vehicle_type):
    vehicle_cost_factor = {
        "kamyonet": 1.0,
        "kamyon": 1.5,
        "kiralik_kamyon": 2.0
    }

    factor = vehicle_cost_factor.get(vehicle_type, 1.0)
    return distance_km * factor
