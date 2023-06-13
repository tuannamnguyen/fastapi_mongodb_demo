from pydantic import BaseModel, Field, EmailStr

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
    