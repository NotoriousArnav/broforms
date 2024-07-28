from pydantic import BaseModel
from typing import Dict, Literal, Annotated
# from bson import ObjectId
from . import MarkdownBlock
from .users import AbstractUser
from datetime import datetime

class BasicFormData(BaseModel):
    data: Dict
    time_submitted: datetime

class FormData(BaseModel):
    title: str
    form_data: MarkdownBlock
    date_created: datetime
    expires_on: datetime
    created_by: str #username

class FormData_(FormData):
    id: str

