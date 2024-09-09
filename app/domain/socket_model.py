from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SocketParams(BaseModel):
    user_name: str


class SocketSession(BaseModel):
    user_name: str
    messaging_user_id: str
    current_channel_id: Optional[str] = None


# event models
class ChannelEventBase(BaseModel):
    channel_id: str


class ChannelOpenEvent(ChannelEventBase):
    pass


class ChannelCloseEvent(ChannelEventBase):
    pass


class ChatEvent(BaseModel):
    channel_id: str
    user_name: str
    query: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
