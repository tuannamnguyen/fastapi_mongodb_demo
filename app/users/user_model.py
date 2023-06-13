from pydantic import BaseModel, EmailStr
from bson import json_util
import json


class UserModel(BaseModel):
    fullname: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Nguyen Tuan Nam",
                "email": "tuannamnguyen290602@gmail.com",
                "password": "abc123"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "tuannamnguyen290602@gmail.com",
                "password": "abc123"
            }
        }


def bson_to_dict(data):
    return json.loads(json_util.dumps(data))
