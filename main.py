from fastapi import FastAPI
from pydantic import BaseModel
import redis

app = FastAPI()
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)


class DataIn(BaseModel):
    phone: str
    address: str


class DataOut(BaseModel):
    address: str


@app.post("/write_data")
async def write_data(data: DataIn):
    redis_db.set(data.phone, data.address)
    return {"message": "Data written successfully"}


@app.get("/check_data")
async def check_data(phone: str):
    address = redis_db.get(phone)
    if address:
        return {"address": address.decode('utf-8')}
    else:
        return {"message": "No data found for the provided phone number"}