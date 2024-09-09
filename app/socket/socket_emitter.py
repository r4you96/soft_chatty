import json

from app.domain.socket_model import ChatEvent
from app.socket.base import server_sio


class SocketServerEventEmitter:
    def __init__(self):
        self.broadcast_room = f'broadcast'

    async def _emit(self, event: str, data: dict):
        await server_sio.emit(event=event,
                              data={'data': data},
                              room=self.broadcast_room)

    async def join_room(self, sid: str):
        await server_sio.enter_room(sid=sid, room=self.broadcast_room)

    async def emit_message(self, event: ChatEvent):
        data = json.loads(event.json(exclude_none=True))
        await self._emit(event='received_message', data=data)
