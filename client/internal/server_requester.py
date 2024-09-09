from typing import List

import httpx

from app.domain.messaging_user import MessagingUser
from client.core.config import config
from app.domain.channel import Channel, ChannelCreate
from client.core.exceptions import ClientException


async def create_channel(channel_name: str) -> Channel:
    async with httpx.AsyncClient() as client:
        body = ChannelCreate(name=channel_name)
        r = await client.post(f'{config.socket_url}/v1/channels',
                              json=body.model_dump())
        if r.status_code != 200:
            raise ClientException(status_code=r.status_code, detail=r.json())
        response = r.json()
        data = response.get('data')
        return Channel(**data)


async def find_channel() -> List[Channel]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{config.socket_url}/v1/channels')

        response = r.json()
        data = response.get('data')
        return [Channel(**channel) for channel in data]


async def read_messaging_user_by_user_name(user_name: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{config.socket_url}/v1/messaging_users/by-name/{user_name}')

        response = r.json()
        data = response.get('data')
        return MessagingUser(**data)
