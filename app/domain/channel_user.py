from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.domain import gen_id


class ChannelUserStatus(str, Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'


class ChannelUser(BaseModel):
    id: str = Field(default_factory=gen_id)
    channel_id: str
    messaging_user_id: str
    status: ChannelUserStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
