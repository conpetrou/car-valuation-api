from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Car(BaseModel):
    vin: str = None
    make: str
    model: str
    year: int
    mileage: int

@app.post("/estimate")
def estimate(car: Car):
    return {
        "estimated_value": 14500 + (2025 - car.year) * -300 - car.mileage * 0.02,
        "source_breakdown": {
            "method": "mocked for local demo"
        }
    }
