from datetime import datetime
from urllib.parse import parse_qsl, urlsplit

from app.domain.channel_user import ChannelUser, ChannelUserStatus
from app.domain.socket_model import SocketParams, SocketSession, ChatEvent, ChannelOpenEvent, ChannelCloseEvent
from app.repository import channel_user_repository
from app.service import messaging_user_service, channel_user_service
from app.socket.base import server_sio
from app.socket.socket_emitter import SocketServerEventEmitter


async def __get_session(sid: str) -> SocketSession:
    session = await server_sio.get_session(sid=sid)
    result = SocketSession(**session)
    return result


async def __set_session(sid: str, session: SocketSession):
    await server_sio.save_session(sid=sid, session=session.model_dump())


def handle_socket_server_events():
    @server_sio.event
    async def connect(sid, environ):
        query_string = environ.get('QUERY_STRING')
        params = dict(parse_qsl(str(urlsplit(query_string).path)))
        connected_params = SocketParams(**params)
        print(f'connected user - {connected_params.user_name}')

        messaging_user = await messaging_user_service.get_or_create_user(user_name=connected_params.user_name)
        session = SocketSession(user_name=connected_params.user_name,
                                messaging_user_id=messaging_user.id)
        await __set_session(sid=sid, session=session)

        event_emitter = SocketServerEventEmitter()
        await event_emitter.join_room(sid=sid)

    @server_sio.event
    async def disconnect(sid):
        session = await __get_session(sid=sid)
        if session.current_channel_id:
            await channel_user_service.close_channel(channel_id=session.current_channel_id,
                                                     messaging_user_id=session.messaging_user_id)
        print(f'disconnect - {session.user_name}')

    @server_sio.on('open_channel')
    async def receive_open_channel(sid: str, data: dict):
        session = await __get_session(sid=sid)
        event = ChannelOpenEvent(**data)

        await channel_user_service.open_channel(channel_id=event.channel_id,
                                                messaging_user_id=session.messaging_user_id,
                                                previous_channel_id=session.current_channel_id)

        session.current_channel_id = event.channel_id
        await __set_session(sid=sid, session=session)

    @server_sio.on('close_channel')
    async def receive_close_channel(sid: str, data: dict):
        session = await __get_session(sid=sid)
        event = ChannelCloseEvent(**data)

        await channel_user_service.close_channel(channel_id=event.channel_id,
                                                 messaging_user_id=session.messaging_user_id)

    @server_sio.on('chat')
    async def receive_message(sid: str, data: dict):
        chat_event = ChatEvent(**data)
        print(f'received message: {chat_event.query}')

        event_emitter = SocketServerEventEmitter()
        await event_emitter.emit_message(event=chat_event)
