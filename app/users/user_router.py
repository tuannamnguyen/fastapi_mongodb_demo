from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from app.users.user_model import *
from app.auth.auth_handler import *
import motor.motor_asyncio

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.demoapp


user_router = APIRouter()

@user_router.get("", status_code=status.HTTP_200_OK)
async def get_all_users():
    return [bson_to_dict(user) async for user in db.users.find()]


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserModel):
    user = jsonable_encoder(user)
    # Insert hashed password into DB
    user.update({"password": get_password_hash(user["password"])})
    await db.users.insert_one(user)
    return bson_to_dict(user)


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(user: UserLoginModel):
    user = jsonable_encoder(user)
    user_in_db = await db.users.find_one({"email": user["email"]})
    if not user_in_db:
        return False
    if not verify_password(user["password"], user_in_db["password"]):
        return False
    return signJWT(user["email"])
