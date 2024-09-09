from urllib.parse import parse_qsl, urlsplit

from app.domain.socket_model import SocketParams, SocketSession, SocketChatEvent, SocketUserMessage
from app.service import messaging_user_service
from app.socket.base import server_sio
from app.socket.socket_emitter import SocketServerEventEmitter


async def __get_session(sid: str) -> SocketSession:
    session = await server_sio.get_session(sid=sid)
    result = SocketSession(**session)
    return result


def handle_socket_server_events():
    @server_sio.event
    async def connect(sid, environ):
        query_string = environ.get('QUERY_STRING')
        params = dict(parse_qsl(str(urlsplit(query_string).path)))
        connected_params = SocketParams(**params)
        print(f'connected user - {connected_params.user_name}')

        messaging_user = await messaging_user_service.get_or_create_user(user_name=connected_params.user_name)
        await server_sio.save_session(sid=sid,
                                      session={'user_name': connected_params.user_name,
                                               'messaging_user_id': messaging_user.id})

        event_emitter = SocketServerEventEmitter()
        await event_emitter.join_broadcast_room(sid=sid)
        await event_emitter.emit_connected()

    @server_sio.event
    async def disconnect(sid):
        session = await __get_session(sid=sid)
        print(f'disconnect - {session.user_name}')

    @server_sio.on('chat')
    async def receive_message(sid: str, data: dict):
        session = await __get_session(sid=sid)
        chat_event = SocketChatEvent(**data)

        print(f'received message: {chat_event.query}')

        event_emitter = SocketServerEventEmitter()
        socket_user_message = SocketUserMessage(user_name=session.user_name,
                                                query=chat_event.query)
        await event_emitter.emit_message(data=socket_user_message)
