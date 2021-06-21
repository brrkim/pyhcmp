from fastapi import FastAPI
from pydantic import BaseModel
from core import sync

class Item(BaseModel):
    tenant_id: str
    instance_name: str = None
    instance_id: str
    instance_addresses: str = None
    instance_az: str
    instance_flavor_id: str
    instance_os_image_id: str = None
    instance_key_name: str = None
    instance_status: str
    
app = FastAPI()

@app.get("/")
async def home():
	return { "message" : "Hello World" }

@app.post("/items")
async def create_item(item: Item):
	return item

@app.get("/items")
async def read_item():
	return sync()