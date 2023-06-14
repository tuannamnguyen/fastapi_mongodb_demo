import time
import jwt
from decouple import config
from passlib.context import CryptContext
from datetime import datetime, timedelta

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_pwd, hashed_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_password_hash(pwd):
    return pwd_context.hash(pwd)


def token_response(token: str) -> dict:
    return {"access_token": token}


def signJWT(user_id: str) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }

    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return decoded_token if decoded_token["expires"] >= time.time() else None

# Replace signJWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else: 
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"expires": expire})
    encoded_token = jwt.encode(to_encode, JWT_SECRET, JWT_ALGORITHM) 
    return {"access_token": encoded_token,"token_type": "bearer"}

