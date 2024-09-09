from typing import Optional, Dict

from pydantic import Field, BaseModel

from app.domain.channel import Channel


class SocketClientStore(BaseModel):
    user_name: Optional[str] = None
    messaging_user_id: Optional[str] = None
    current_channel: Optional[Channel] = None
    channels: Dict[str, Channel] = Field(default_factory=dict)


client_store = SocketClientStore()
