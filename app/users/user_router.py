from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from app.users.user_model import *
from app.auth.auth_handler import *
from typing import Annotated
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
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_in_db = bson_to_dict(await db.users.find_one({"username": form_data.username}))
    authenticated = authenticate_user(user_in_db, form_data.password)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires = timedelta(minutes=30)
    return create_access_token(user_in_db, expires_delta=expires)
