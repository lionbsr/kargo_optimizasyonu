from algorithms.distributor import distribute_cargos
from algorithms.vehicle import VEHICLES
from algorithms.optimizer import fetch_cargos

cargos = fetch_cargos()
vehicles = distribute_cargos(cargos, VEHICLES)

for v in vehicles:
    print(f"\n🚚 Araç {v['id']} ({v['capacity']} kg)")
    print(f"Yüklenen: {v['used']} kg")

    for c in v["cargos"]:
        print(f" - Kargo {c['id']} ({c['station']}) {c['weight']} kg")
