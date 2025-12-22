class Vehicle:
    def __init__(self, vehicle_id, capacity, rent_cost=0):
        self.id = vehicle_id
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.rent_cost = rent_cost
        self.cargos = []
        self.stations = set()

    def can_take(self, cargo):
        return self.remaining_capacity >= cargo["weight"]

    def add_cargo(self, cargo):
        self.cargos.append(cargo)
        self.stations.add(cargo["station"])
        self.remaining_capacity -= cargo["weight"]

    def total_weight(self):
        return sum(c["weight"] for c in self.cargos)
