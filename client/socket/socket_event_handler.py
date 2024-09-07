from app.domain.socket_model import SocketUserMessage
from client.socket.base import sio


def handle_socket_client_events():
    @sio.on('connected')
    async def receive_connected_event():
        print('succeed connect to server')

    @sio.on('received_message')
    async def received_message(data: dict):
        user_message = SocketUserMessage(**data.get('data'))
        print(f'{user_message.user_name}: {user_message.query}')
