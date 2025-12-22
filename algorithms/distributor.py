def distribute_cargos(cargos, vehicles):
    """
    cargos: [
        {id, weight, station}
    ]
    vehicles: [
        {id, capacity, used, cargos}
    ]
    """

    # 🔹 Kargoları büyükten küçüğe sırala
    cargos = sorted(cargos, key=lambda c: c["weight"], reverse=True)

    for cargo in cargos:
        selected_vehicle = None
        min_used = float("inf")

        for vehicle in vehicles:
            if vehicle["used"] + cargo["weight"] <= vehicle["capacity"]:
                if vehicle["used"] < min_used:
                    min_used = vehicle["used"]
                    selected_vehicle = vehicle

        if selected_vehicle:
            selected_vehicle["cargos"].append(cargo)
            selected_vehicle["used"] += cargo["weight"]
        else:
            cargo["rejected"] = True  # kapasite yetmedi

    return vehicles
