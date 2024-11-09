from core.classes import Fuels,Powerplant
from typing import List

def solve(powerplants_list: List[Powerplant], load: int, fuels: Fuels):
    for plant in powerplants_list:
        plant.price = plant.get_cost_per_mwh(fuels)

    sorted_plants = sorted(powerplants_list, key = lambda x: x.price)
    total_cost = 0
    # Assign power to each plant in order of price
    for plant in sorted_plants:
        min_power, max_power = plant.get_available_power(fuels)
        if load > 0:
            usable_power = min(max_power, load) # Try to use maximum possible power from this plant
            if usable_power >= min_power:
                plant.injection = round(usable_power,2)
                load -= usable_power
                total_cost += usable_power * plant.price
            else:
                plant.injection = 0
        else:
            plant.injection = 0

    # total_cost
    # total_power = sum(p.injection for p in sorted_plants)
    # load_met = abs(total_power - load.value) < 0.1,
    return sorted_plants
