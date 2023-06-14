from pydantic import BaseModel
from bson import json_util
import json


class UserModel(BaseModel):
    fullname: str
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Nguyen Tuan Nam",
                "email": "tuannamnguyen290602",
                "password": "abc123"
            }
        }


def bson_to_dict(data):
    return json.loads(json_util.dumps(data))
