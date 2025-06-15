from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI()

VIN_API_KEY = "bb00733ff350"

class CarInput(BaseModel):
    vin: str | None = None
    make: str | None = None
    model: str | None = None
    submodel: str | None = None
    year: int | None = None
    mileage: float
    mileage_unit: str  # "km" or "mi"
    fuel_type: str | None = None
    transmission: str | None = None
    condition: str | None = None
    trim: str | None = None

@app.post("/estimate")
def estimate_car_value(data: CarInput):
    # If VIN is provided, decode it
    if data.vin:
        vin_url = f"https://api.vindecoder.eu/2.0/{VIN_API_KEY}/{data.vin}.json"
        response = requests.get(vin_url)

        if response.status_code == 200:
            vin_data = response.json()
            details = vin_data.get("decode", {})

            data.make = details.get("make", data.make)
            data.model = details.get("model", data.model)
            data.submodel = details.get("version", data.submodel)
            data.year = int(details.get("year", data.year or 0))
            data.fuel_type = details.get("fueltype", data.fuel_type)
            data.transmission = details.get("gearbox", data.transmission)
            data.trim = details.get("equipment", data.trim)
        else:
            return {"error": "Failed to decode VIN"}

    # Fallback/default values if anything is missing
    if not data.make or not data.model or not data.year:
        return {"error": "Missing key information to estimate value."}

    # Simulated valuation logic
    base_price = 30000
    age_penalty = (2025 - data.year) * 700
    mileage_penalty = data.mileage * (0.05 if data.mileage_unit == "km" else 0.08)
    condition_modifier = {
        "excellent": 1.1,
        "good": 1.0,
        "fair": 0.9,
        "poor": 0.7
    }.get(data.condition or "good", 1.0)

    estimated_value = (base_price - age_penalty - mileage_penalty) * condition_modifier
    estimated_value = max(estimated_value, 1000)  # Set minimum value

    return {"estimated_value": round(estimated_value, 2)}
