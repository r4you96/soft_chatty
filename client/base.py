import asyncio
import sys

from client.internal import server_requester
from client.sevice import channel_service, message_service
from client.socket import socket_emitter
from client.socket.base import sio
from client.socket.socket_event_handler import handle_socket_client_events
from client.socket.store import client_store
from client.util.async_util import read_input


async def handle_input_events():
    while True:
        user_input = await read_input()
        try:
            split_input = user_input.split()
            event = split_input[0]
            event_value = ' '.join(split_input[1:]).strip()
        except Exception as e:
            continue

        # base events
        if event == 'close':
            await socket_emitter.close()
            break

        # channel events
        if event == 'create_channel':
            await channel_service.create(channel_name=event_value)
        elif event == 'show_channels':
            await channel_service.show_channels()
        elif event == 'open_channel':
            await channel_service.open_channel(channel_name=event_value)
        elif event == 'close_channel':
            await channel_service.close_channel()

        # msg event
        if event == 'msg':
            await message_service.send_message(query=event_value)


async def init_socket(user_name: str):
    await socket_emitter.connect(user_name=user_name)
    messaging_user = await server_requester.read_messaging_user_by_user_name(user_name=user_name)
    client_store.messaging_user_id = messaging_user.id
    client_store.user_name = user_name
    await channel_service.show_channels()


async def run_client():
    print('insert user_name')
    user_name = sys.stdin.readline().strip()
    await init_socket(user_name=user_name)

    handle_socket_client_events()
    await asyncio.gather(
        handle_input_events(),
        sio.wait()
    )
