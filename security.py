from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated, Union
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from db import db
from schemas.users import User
from datetime import datetime, timedelta, timezone
import os
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
ph = PasswordHasher()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False

def getUser(username: str) -> User:
    user = db.users.find_one(
        {
            'username': username
        }
    )
    if not user:
        return None
    return User(**user)

def authenticateUser(username: str, password: str) -> Union[User, bool]:
    user = getUser(username)
    if not user:
        return False
    if verify_password(password, user.password):
        return user
    else:
        False

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update(
        {
            "exp": expire
        }
    )
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY", "secret"),
        algorithm="HS256"
    )
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = getUser(username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.deactivated:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
