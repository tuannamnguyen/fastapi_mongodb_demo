import time

import jwt
from decouple import config
from passlib.context import CryptContext

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_pwd, hashed_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_password_hash(pwd):
    return pwd_context.hash(pwd)


def authenticate_user(user_in_db: dict, password: str) -> bool:
    if not user_in_db:
        return False
    if not verify_password(password, user_in_db["password"]):
        return False
    return True


def create_access_token(data: dict, expires_delta: float | None = None):
    to_encode = {"fullname": data["fullname"],
                 "username": data["username"]}
    if expires_delta:
        expire = time.time() + expires_delta
    else:
        expire = time.time() + 900
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, JWT_SECRET, JWT_ALGORITHM)
    return {"access_token": encoded_token, "token_type": "bearer"}
