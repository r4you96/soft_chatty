from typing import List

import httpx

from app.domain.message import Message
from app.domain.messaging_user import MessagingUser
from client.core.config import config
from app.domain.channel import Channel, ChannelCreate, ChannelForClient
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


async def find_channel() -> List[ChannelForClient]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{config.socket_url}/v1/channels',
                             params={'for_client': True})

        response = r.json()
        data = response.get('data')
        return [ChannelForClient(**channel) for channel in data]


async def read_messaging_user_by_user_name(user_name: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{config.socket_url}/v1/messaging_users/by-name/{user_name}')

        response = r.json()
        data = response.get('data')
        return MessagingUser(**data)


async def find_message(channel_id: str) -> List[Message]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{config.socket_url}/v1/messages',
                             params={'channel_id': channel_id})

        response = r.json()
        data = response.get('data')
        return [Message(**message) for message in data]
