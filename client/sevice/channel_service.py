from app.domain.socket_model import ChannelOpenEvent, ChannelCloseEvent
from client.core.exceptions import ClientException
from client.internal import server_requester
from client.socket import socket_emitter
from client.socket.store import client_store


async def create(channel_name: str):
    try:
        channel = await server_requester.create_channel(channel_name=channel_name)
    except ClientException as e:
        print(f'status_code - {e.status_code}, {e.detail}')
        return
    print(f'succeed channel create - {channel}')
    client_store.channels[channel.id] = channel


async def show_channels():
    channels = await server_requester.find_channel()
    client_store.channels = {
        channel.id: channel
        for channel in channels
    }
    print('---channels--')
    for idx, channel in enumerate(channels):
        print(f'[{idx + 1}] {channel.name}')
    print('-------')


async def open_channel(channel_name: str):
    if client_store.current_channel and client_store.current_channel.name == channel_name:
        print(f'Already enter channel - {channel_name}')
        return

    channels_by_name = {
        channel.name: channel
        for channel in client_store.channels.values()
    }
    exist_channel = channels_by_name.get(channel_name)
    if not exist_channel:
        print(f'Not exist channel - {channel_name}')
        return

    event = ChannelOpenEvent(channel_id=exist_channel.id)
    await socket_emitter.open_channel(event=event)
    client_store.current_channel = exist_channel
    print(f'current channel - {channel_name}')


async def close_channel():
    if not client_store.current_channel:
        print('There are no channels currently opened')
        return
    event = ChannelCloseEvent(channel_id=client_store.current_channel.id)
    await socket_emitter.close_channel(event=event)
    print(f'current channel - None')
    client_store.current_channel = None

