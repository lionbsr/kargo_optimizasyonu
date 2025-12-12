VEHICLES = [
    {"capacity": 500, "rent_cost": 0},
    {"capacity": 750, "rent_cost": 0},
    {"capacity": 1000, "rent_cost": 0},
]

RENTED_VEHICLE = {"capacity": 500, "rent_cost": 200}


def assign_vehicle(total_weight):
    capacity_sum = sum(v["capacity"] for v in VEHICLES)

    if total_weight <= capacity_sum:
        return VEHICLES, 0
    else:
        return VEHICLES + [RENTED_VEHICLE], RENTED_VEHICLE["rent_cost"]
