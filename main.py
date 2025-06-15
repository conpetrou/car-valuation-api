from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import requests

app = FastAPI()

# Allow all CORS origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "bb00733ff350"
SECRET_KEY = "38f4e93d23"

@app.get("/")
def root():
    return {"message": "VIN Decoder API"}

@app.get("/decode-vin/{vin}")
def decode_vin(vin: str):
    vin = vin.upper()
    section = "info"
    id = "info"

    # Compute control sum using SHA1
    hash_string = f"{vin}|{id}|{API_KEY}|{SECRET_KEY}"
    control_sum = hashlib.sha1(hash_string.encode()).hexdigest()[:10]

    # API URL
    url = f"https://api.vindecoder.eu/3.2/{API_KEY}/{control_sum}/decode/{section}/{vin}.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Optional: Check if VIN was successfully decoded
        if "decode" not in data or not data["decode"]:
            raise HTTPException(status_code=404, detail="VIN details not found")

        return data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    