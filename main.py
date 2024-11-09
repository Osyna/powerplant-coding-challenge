from dataclasses import dataclass
import json
from typing import List
from fastapi import FastAPI


app = FastAPI()


@dataclass
class Load:
    value: int


@dataclass
class Fuels:
    gas: int
    kerosine: int
    co2: int
    wind: int


@dataclass
class Powerplant:
    pid: int # Not Used Here but might be use for Slack Bus when Loss = Load + cable length
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int
    injection: float = 0
    price: float = 0

    def get_cost_per_mwh(self, fuels: Fuels) -> float:
        """Calculate cost / MWh based on fuel type and efficiency"""
        costs = {
            'gasfired':    fuels.gas / self.efficiency,
            'turbojet':    fuels.kerosine / self.efficiency,
            'windturbine': 0
            }
        return costs[self.type]

    def get_available_power(self, fuels: Fuels) -> tuple[float, float]:
        """Returns (min, max) available power """
        if self.type == 'windturbine':
            max_power = self.pmax * (fuels.wind / 100.0)
            return 0, max_power
        return self.pmin, self.pmax


@app.get("/productionplan")
def api_response():
    path = './example_payloads/payload3.json'
    load, fuels_stat, powerplants_list = load_data(path)
    solve(powerplants_list=powerplants_list, load=load, fuels=fuels_stat)
    return {pw.name:pw.injection for pw in powerplants_list}


def solve(powerplants_list: List[Powerplant], load: Load, fuels: Fuels):
    for plant in powerplants_list:
        plant.price = plant.get_cost_per_mwh(fuels)

    sorted_plants = sorted(powerplants_list, key = lambda x: x.price)
    remaining_load = load.value
    total_cost = 0

    # Assign power to each plant in order of price
    for plant in sorted_plants:
        min_power, max_power = plant.get_available_power(fuels)

        if remaining_load > 0:
            usable_power = min(max_power, remaining_load) # Try to use maximum possible power from this plant
            if usable_power >= min_power:
                plant.injection = round(usable_power,2)
                remaining_load -= usable_power
                total_cost += usable_power * plant.price
            else:
                plant.injection = 0
        else:
            plant.injection = 0

    # total_cost
    # total_power = sum(p.injection for p in sorted_plants)
    # load_met = abs(total_power - load.value) < 0.1,
    return sorted_plants

def load_data(path: str):
    with open(path, 'r') as file:
        payload = json.load(file)
    load = Load(payload['load'])
    fuels_stat = Fuels(*payload['fuels'].values())
    powerplants_list = [Powerplant(i + 1, **pw) for i, pw in enumerate(payload['powerplants'])]
    return load,fuels_stat,powerplants_list





