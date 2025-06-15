from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow all origins for dev purposes — secure it later in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CarDetails(BaseModel):
    vin: str | None = None
    make: str
    model: str
    submodel: str | None = None
    year: int
    mileage: float
    mileage_unit: str  # "km" or "mi"
    fuel_type: str
    transmission: str
    condition: str
    trim: str

@app.post("/estimate")
async def estimate_car_value(details: CarDetails):
    mileage_km = details.mileage * 1.60934 if details.mileage_unit == "mi" else details.mileage

    # Simple scoring mock (adjust with real ML or logic later)
    base_value = 10000
    age_penalty = (2025 - details.year) * 500
    mileage_penalty = (mileage_km // 10000) * 300
    condition_bonus = {"excellent": 1500, "good": 700, "fair": 0, "needs repair": -1000}
    trim_bonus = {"basic": 0, "mid-range": 800, "full-spec": 1500, "custom": 1000}

    estimated_value = base_value - age_penalty - mileage_penalty
    estimated_value += condition_bonus.get(details.condition.lower(), 0)
    estimated_value += trim_bonus.get(details.trim.lower(), 0)

    # Final rounding
    estimated_value = max(estimated_value, 1000)

    return {"estimated_value": round(estimated_value, 2)}
