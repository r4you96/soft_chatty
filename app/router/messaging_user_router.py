from fastapi import APIRouter, HTTPException

from app.domain.response_model import ResponseModel
from app.repository import messging_user_repository


router = APIRouter()


@router.get('/by-name/{user_name}')
async def read_channel_by_user_name(user_name: str):
    messaging_user = await messging_user_repository.read_by_user_name(user_name=user_name)
    if not messaging_user:
        raise HTTPException(status_code=404, detail=f'Not exist user - {user_name}')

    return ResponseModel(data=messaging_user)
