from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.utils import format_payload
from core.func import solve
from typing import Dict, Any
import os

# https://fastapi.tiangolo.com/#recap
productionApp = FastAPI()

class ProductionPlanRequest(BaseModel):
    load: float
    fuels: Dict[str, Any]
    powerplants: list[dict]

@productionApp.get("/")
async def default():
    endpoint = os.getenv('API_ENDPOINT', 'productionplan')
    return {'message': f'do post request to /{endpoint}'}

@productionApp.post("/{endpoint}")
async def get_productionplan(endpoint: str, payload: ProductionPlanRequest):
    if endpoint != os.getenv('API_ENDPOINT', 'productionplan'):
        raise HTTPException(status_code = 404, detail = "Endpoint not found")
    load, fuels_stat, powerplants_list = format_payload(payload)
    solve(powerplants_list = powerplants_list, load = load, fuels = fuels_stat)
    return {pw.name: pw.injection for pw in powerplants_list}