from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional

class PyObjectId(ObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    username: str
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        
class Provider(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    vendor: str
    userid: str
    userpw: str
    apikey: str
    secret: str
    region: str = None
    
    class Config:
        arbitrary_types_allowed = True
        require_by_default = False
        json_encoders = {
            ObjectId: str
        }
    
class Server(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    tenant_id: str
    instance_name: str = None
    instance_id: str
    instance_addresses: str = None
    instance_az: str
    instance_flavor_id: str
    instance_os_image_id: str = None
    instance_key_name: str = None
    instance_status: str
    created: datetime = None
    updated: datetime = None
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }