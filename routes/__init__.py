from fastapi import APIRouter
from .forms import router as form_router
from .auth import router as auth_router

router = APIRouter()

router.include_router(form_router)
router.include_router(auth_router)
