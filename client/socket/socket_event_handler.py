from datetime import datetime

from app.domain.socket_model import ChatEvent
from client.socket.base import sio
from client.socket.store import client_store


def handle_socket_client_events():
    @sio.on('received_message')
    async def received_message(data: dict):
        chat_event = ChatEvent(**data.get('data'))
        if not client_store.current_channel or client_store.current_channel.id != chat_event.channel_id:
            return
        if chat_event.user_name == client_store.user_name:
            return
        print(f'{chat_event.user_name}[{datetime.strftime(chat_event.created_at, "%H:%M:%S")}]: {chat_event.query}')
