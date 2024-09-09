from typing import List

from fastapi import APIRouter, HTTPException

from app.domain.channel import Channel, ChannelCreate
from app.domain.response_model import ResponseModel
from app.repository import channel_repository

router = APIRouter()


@router.post('')
async def create_channel(body: ChannelCreate) -> ResponseModel[Channel]:
    exist_channel = await channel_repository.read_by_name(channel_name=body.name)
    if exist_channel:
        raise HTTPException(status_code=400, detail=f'Already exist channel name - {body.name}')

    channel_create = Channel(name=body.name)
    await channel_repository.create(channel=channel_create)

    return ResponseModel(data=channel_create)


@router.get('')
async def find_channels() -> ResponseModel[List[Channel]]:
    channels = await channel_repository.find_channel()
    return ResponseModel(data=channels)
