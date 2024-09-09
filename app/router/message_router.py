from fastapi import APIRouter

from app.domain.response_model import ResponseModel
from app.repository import message_repository

router = APIRouter()


@router.get('')
async def find_message(channel_id: str):
    messages = await message_repository.find(channel_id=channel_id)
    return ResponseModel(data=messages)
