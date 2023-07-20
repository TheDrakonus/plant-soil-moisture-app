from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import Database

app = FastAPI()
db = Database()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/devices")
def get_devices():
    return db.get_devices()

@app.get("/devices/{device_id}")
def get_device_by_id(device_id: int):
    return db.get_device_by_id(device_id)

@app.get("/devices/{device_id}/sensor_data")
def get_device_sensor_data(device_id: int):
    return db.get_device_sensor_data(device_id)

@app.get("/devices/mac/{mac}")
def get_device_by_mac(mac: str):
    return db.get_device_by_mac(mac)

@app.get("/devices/{device_id}/temperature_moisture_logs")
def get_temperature_moisture_logs(device_id: int):
    data = db.get_temperure_moisture_logs(device_id)
    if data is None:
        return {"error": "Device not found"}
    return data
