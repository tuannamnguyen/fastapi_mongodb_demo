from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from app.users.user_model import *
from app.auth.auth_handler import *
from app.auth.auth_bearer import jwt_validator
from typing import Annotated
from decouple import config
import motor.motor_asyncio

DB_CONNECTION_STRING = config("db_connection_string")

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
db = client.demoapp

user_router = APIRouter()


@user_router.get("", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
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
    if user_in_db is not None:
        authenticated = authenticate_user(user_in_db, form_data.password)
        if not authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        expires = 600
        return create_access_token(user_in_db, expires_delta=expires)
    return {"detail": "User not found"}


@user_router.delete("/{username}", dependencies=[Depends(jwt_validator)], status_code=status.HTTP_200_OK)
async def delete_user_by_username(username: str) -> dict:
    user = await db.users.find_one({"username": username})
    if user is not None:
        await db.users.delete_one({"username": username})
        return bson_to_dict(user)
    raise HTTPException(
        status_code=404, detail=f"User {username} not found")
