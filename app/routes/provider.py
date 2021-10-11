from fastapi import APIRouter
from pydantic import BaseModel
from app.database.conn import mongo
from app.models import Provider,PyObjectId,Server
from app.internal.core import build_provider_resources,discover_brownfields

router = APIRouter()

@router.get("/provider")
async def retrieve_all_providers():
    providers = []
    for provider in mongo.get_db().providers.find():
        providers.append(Provider(**provider))
    return {'providers': providers}

@router.get("/provider/{id}")
async def retrieve_single_provider(id: str):
    provider = mongo.get_db().providers.find_one({"_id": PyObjectId(id)})
    return {'provider': Provider(**provider)}

# @router.get("/provider/sync")
# async def sync_all_providers():
#     providers = []
#     for provider in mongo.get_db().providers.find():
#         providers.append(Provider(**provider))
#     return {'providers': providers}

@router.get("/provider/sync/{id}")
async def sync_single_provider(id: str):
    provider = mongo.get_db().providers.find_one({"_id": PyObjectId(id)})
    resources = build_provider_resources(provider)
    browndfields = discover_brownfields(resources)
    bf_list = list(map(dict, [bf for bf in browndfields]))
    result = mongo.get_db().servers.insert_many(bf_list)
    inserted_count = len(result.inserted_ids)
    return {"status": "success","message":f"inserted {inserted_count} server(s)"}

    
@router.post("/provider")
async def create_single_provider(provider : Provider):
    if hasattr(provider, 'id'):
        delattr(provider, 'id')
    result = mongo.get_db().providers.insert_one(provider.dict(by_alias=True))
    provider.id = result.inserted_id
    return {'provider': provider}

# @router.put("/providers/{id}")
# async def update_providers(id: str):
#     provider = mongo.get_db().providers.find_one({"_id": PyObjectId(id)})
#     if provider:
#         mongo.get_db().providers.update_one({"_id": PyObjectId(id)})
#     return {'status': "success"}

@router.delete("/provider")
async def delete_all_providers():
    result = mongo.get_db().providers.delete_many({"region": None})
    deleted_count = result.deleted_count
    return {"status": "success","message":f"deleted {deleted_count} provider(s)"}

@router.delete("/provider/{id}")
async def delete_single_provider(id: str):
    provider = mongo.get_db().providers.find_one({"_id": PyObjectId(id)})
    if provider:
        result = mongo.get_db().providers.delete_one({"_id": PyObjectId(id)})
        return {"status": "success","message":result}
    else:
        return {"status": "fail","message":"no provider matched"}
