from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.domain import gen_id
from app.domain.message import Message


class Channel(BaseModel):
    id: str = Field(default_factory=gen_id)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChannelCreate(BaseModel):
    name: str


class ChannelForClient(Channel):
    active_count: int
    last_message: Optional[Message] = None
