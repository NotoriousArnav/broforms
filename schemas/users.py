from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime
from typing import Union
# from bson import ObjectId

class BasicUser(BaseModel):
    username: str
    password: str
    time_created: datetime

class AbstractUser(BasicUser):
    email: Union[EmailStr, None] = None
    phone: Union[None, PhoneNumber] = None
    deactivated: bool = False

class User(AbstractUser):
    bio: Union[str, None] = None
    name: str
    email_verified: bool = False
    phone_verified: bool = False


class UserForm(BaseModel):
    username: str
    password: str
    email: Union[None, EmailStr] = None
    phone: Union[None, PhoneNumber]= None
    bio: Union[str, None] = None
    name: str = None
