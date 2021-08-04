from fastapi import APIRouter
from pydantic import BaseModel
from app.database.conn import mongo
from app.models import User

router = APIRouter()

@router.get('/user')
async def list_user():
    users = []
    for user in mongo.get_db().users.find():
        users.append(User(**user))
    return {'user': users}

@router.post('/user')
async def create_user(user: User):
    if hasattr(user, 'id'):
        delattr(user, 'id')
    ret = mongo.get_db().user.insert_one(user.dict(by_alias=True))
    user.id = ret.inserted_id
    return {'user': user}