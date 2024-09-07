import asyncio
import sys

from client.socket.base import sio
from client.socket.socket_emitter import SocketClientEmitter
from client.socket.socket_event_handler import handle_socket_client_events
from client.util.async_util import read_input


async def handle_input():
    while True:
        user_input = await read_input()
        split_input = user_input.split()
        event = split_input[0]
        if event == 'close':
            await SocketClientEmitter.close_socket()
            break

        if event == 'msg':
            query = ''.join(split_input[1:])
            await SocketClientEmitter.send_message(query=query)


async def run_client():
    print('insert user_name : ')
    user_name = sys.stdin.readline().strip()
    await SocketClientEmitter.connect(user_name=user_name)
    handle_socket_client_events()

    await asyncio.gather(
        handle_input(),
        sio.wait()
    )
