from app.domain.socket_model import ChatEvent
from client.socket import socket_emitter
from client.socket.store import client_store


async def send_message(query: str):
    if not client_store.current_channel:
        print('Any entered channel')
        return
    event = ChatEvent(channel_id=client_store.current_channel.id,
                      user_name=client_store.user_name,
                      messaging_user_id=client_store.messaging_user_id,
                      query=query)
    await socket_emitter.send_message(event=event)
