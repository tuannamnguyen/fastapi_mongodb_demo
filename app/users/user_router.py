from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from app.users.user_model import *
from app.auth.auth_handler import *
import motor.motor_asyncio

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.demoapp


user_router = APIRouter()


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel):
    user = jsonable_encoder(user)
    user.update({"password": get_password_hash(user["password"])})
    await db.users.insert_one(user)
    return bson_to_dict(user)
