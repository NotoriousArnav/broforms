from pydantic import BaseModel
from .users import AbstractUser

class MarkdownBlock(BaseModel):
    title: str
    content: str
    stylesheet: str = None
