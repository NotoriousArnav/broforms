from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(
    tags=[
        "template"
    ]
)

__import__('pprint').pprint(os.system('pwd'))

templates = Jinja2Templates(
    directory="templates"
)

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )
