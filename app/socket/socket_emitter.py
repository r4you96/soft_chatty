from app.domain.socket_model import SocketUserMessage
from app.socket.base import server_sio


class SocketServerEventEmitter:
    def __init__(self):
        self.broadcast_room = 'broadcast_room'

    async def _emit(self, event: str, data: dict):
        await server_sio.emit(event=event,
                              data={'data': data},
                              room=self.broadcast_room)

    async def join_broadcast_room(self, sid: str):
        await server_sio.enter_room(sid=sid, room=self.broadcast_room)

    async def emit_connected(self):
        await self._emit(event='connected', data={})

    async def emit_message(self, data: SocketUserMessage):
        dumped_data = data.model_dump(exclude_none=True)
        await self._emit(event='received_message', data=dumped_data)
