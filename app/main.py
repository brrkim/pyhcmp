from fastapi import FastAPI
from pydantic import BaseModel
from core import build_provider_resource,discover_brownfields
    
app = FastAPI()

@app.get("/")
async def home():
	return { "message" : "Hello World" }

@app.get("/build")
async def read_item():
    provider_server = build_provider_resource()

@app.get("/items")
async def read_item():
    return discover_brownfields(provider_server)
