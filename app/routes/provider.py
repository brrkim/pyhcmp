from fastapi import APIRouter
from pydantic import BaseModel
from app.database.conn import mongo
from app.models import Provider,PyObjectId,Server
from app.internal.core import build_provider_resource,discover_brownfields

router = APIRouter()

@router.get("/provider")
async def list_provider():
    providers = []
    for provider in mongo.get_db().providers.find():
        providers.append(Provider(**provider))
    return {'providers': providers}
    
@router.post("/provider")
async def create_provider(provider : Provider):
    if hasattr(provider, 'id'):
        delattr(provider, 'id')
    ret = mongo.get_db().providers.insert_one(provider.dict(by_alias=True))
    provider.id = ret.inserted_id
    return {'provider': provider}

# @router.put("/providers/{id}")
# async def update_providers(id: str):
#     provider = mongo.get_db().providers.find_one({"_id": PyObjectId(id)})
#     if provider:
#         mongo.get_db().providers.update_one({"_id": PyObjectId(id)})
#     return {'status': "success"}

@router.delete("/provider/{id}")
async def delete_provider(id: str):
    provider = mongo.get_db().providers.find_one({"_id": PyObjectId(id)})
    if provider:
        mongo.get_db().providers.delete_one({"_id": PyObjectId(id)})
    return {'status': "success"}