from fastapi import APIRouter, HTTPException, Depends
from schemas.forms import FormData, FormData_
from schemas.users import User
from db import db
from bson import ObjectId
from typing import List, Dict
from security import get_current_active_user

router = APIRouter(
    prefix="/forms",
    tags=[
        "forms"
    ]
)

@router.get('/{id}', response_model=FormData_)
async def form_info(id: str):
    form = db.forms.find_one(
        {
            '_id': ObjectId(id)
        }
    )
    form['id'] = str(form['_id'])
    Form = FormData_(**form)
    Form.id = id
    return Form

@router.post('/')
async def post_form(data: FormData, user: User = Depends(get_current_active_user)):
    data.created_by = user.username
    id = db.forms.insert_one(
        data.dict()
    ).inserted_id
    dt = data.dict()
    dt['id'] = str(id)
    form = FormData_(**dt)
    return form

@router.post('/{id}')
async def form_response_take(id: str, data: dict):
    form = db.forms.find_one(
        {
            '_id': ObjectId(id)
        }
    )
    if not form:
        raise HTTPException(
            status_code=404,
            detail="form not found"
        )
    db.responses.insert_one(
        {
            'response': data,
            'form_id': id
        }
    ).inserted_id
    return {
        'message': 'response submitted'
    }

@router.get('/{id}/responses', response_model=List[Dict])
async def getResponses(id: str, user: User = Depends(get_current_active_user)):
    form = db.forms.find_one(
        {
            '_id': ObjectId(id)
        }
    )
    if not form:
        raise HTTPException(
            status_code=404,
            detail="form not found"
        )
    if form['created_by'] != user.username:
        raise HTTPException(
            status_code=403,
            detail="forbidden"
        )
    responses =db.responses.find(
            {
                'form_id': id
            }
        )
    results = []
    for response in responses:
        response['id'] = str(response['_id'])
        del response['_id']
        results.append(response)
    return results
