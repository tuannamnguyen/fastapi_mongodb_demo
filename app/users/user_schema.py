from pydantic import BaseModel


class UserSchema(BaseModel):
    fullname: str
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Nguyen Tuan Nam",
                "username": "tuannamnguyen290602",
                "password": "abc123"
            }
        }
