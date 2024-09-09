import json

from app.domain.socket_model import ChannelOpenEvent, ChannelCloseEvent, ChatEvent
from client.core.config import config
from client.socket.base import sio


async def connect(user_name: str):
    url = f'{config.socket_url}?user_name={user_name}'
    await sio.connect(url=url,
                      transports=['websocket'])
    print('connected server')


async def close():
    await sio.disconnect()


async def open_channel(event: ChannelOpenEvent):
    await sio.emit(event='open_channel', data=event.model_dump())


async def close_channel(event: ChannelCloseEvent):
    await sio.emit(event='close_channel', data=event.model_dump())


async def send_message(event: ChatEvent):
    data = json.loads(event.json(exclude_none=True))
    await sio.emit(event='chat', data=data)




