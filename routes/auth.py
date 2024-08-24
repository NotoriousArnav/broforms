from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security import *
from schemas.users import User, UserForm
from schemas.forms import FormData_
from db import db
from datetime import datetime, timedelta, timezone
from typing import List

router = APIRouter(
    prefix="/auth",
    tags=[
        "auth"
    ]
)

@router.post("/signup", response_model=User)
async def signup(form_data: UserForm):
    u = getUser(form_data.username)
    if u:
        raise HTTPException(status_code=400, detail="Username already taken")
    form_data.password = ph.hash(form_data.password)
    data = form_data.dict()
    data['time_created'] = datetime.now(timezone.utc)
    user = User(**data)
    db.users.insert_one(user.dict())
    del user.__dict__['password']
    return user


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    del current_user.__dict__['password']
    return current_user

@router.get('/me/forms', response_model=List[FormData_])
async def getForms(user: User = Depends(get_current_user)):
    forms = db.forms.find(
        {
            'created_by': user.username
        }
    )
    results = []
    for form in forms:
        form['id'] = str(form['_id'])
        del form['_id']
        results.append(FormData_(**form))
    return results

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.getenv('JWT_DURATION', 5)))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }

