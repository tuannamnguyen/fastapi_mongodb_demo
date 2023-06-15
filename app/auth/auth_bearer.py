from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jwt import PyJWTError

from app.auth.auth_handler import *
from decouple import config
import motor.motor_asyncio

DB_CONNECTION_STRING = config("db_connection_string")

# Connect to DB
client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
db = client.demoapp

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def jwt_validator(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("username")
        expire_time: float = payload.get("exp")
        if username is None or expire_time <= time.time():
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = await db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
