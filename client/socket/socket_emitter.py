from client.core.config import config
from client.socket.base import sio


class SocketClientEmitter:
    @staticmethod
    async def connect(user_name: str):
        url = f'{config.socket_url}?user_name={user_name}'
        await sio.connect(url=url,
                          transports=['websocket'])

    @staticmethod
    async def close_socket():
        await sio.disconnect()

    @staticmethod
    async def send_message(query: str):
        data = {'query': query}
        await sio.emit(event='chat', data=data)
