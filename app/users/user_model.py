from pydantic import BaseModel


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


def bson_to_dict(data) -> dict:
    return {
        "id": str(data.get("_id")),
        "fullname": data.get("fullname"),
        "username": data.get("username"),
        "password": data.get("password")
    }
