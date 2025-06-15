from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CarData(BaseModel):
    vin: str
    make: str
    model: str
    year: int
    mileage: int

@app.post("/estimate")
def estimate_value(data: CarData):
    current_year = 2025
    age = current_year - data.year
    mileage_penalty = data.mileage * 0.03  # €0.03 per km
    age_penalty = age * 500  # €500 per year

    # Base value per brand (just examples)
    base_prices = {
        "toyota": 18000,
        "bmw": 25000,
        "mercedes": 26000,
        "audi": 24000,
        "ford": 17000,
        "honda": 18500,
        "nissan": 18000,
        "volkswagen": 20000,
    }

    make_key = data.make.lower()
    base_price = base_prices.get(make_key, 19000)  # default if make not found

    estimated_value = base_price - age_penalty - mileage_penalty

    # Never go below €2,000
    estimated_value = max(estimated_value, 2000)

    return {"estimated_value": round(estimated_value, 2)}
