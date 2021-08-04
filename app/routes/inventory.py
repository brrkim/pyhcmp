from fastapi import APIRouter
from pydantic import BaseModel
from app.database.conn import mongo
from app.models import Provider,PyObjectId,Server
from app.internal.core import build_provider_resource,discover_brownfields

router = APIRouter()

@router.get("/sync")
async def sync_resource():
    servers = []
    for provider in mongo.get_db().providers.find():
        servers += build_provider_resource(provider)
    response = discover_brownfields(servers)
    # for r in response:
    #     ret = mongo.get_db().servers.insert_one(r.dict(by_alias=True))
    #     r.inserted_id = ret.inserted_id
    return {'servers': response}

@router.get("/server")
async def list_server():
    servers = []
    for server in mongo.get_db().servers.find():
        servers.append(Server(**server))
    return {'servers': servers}