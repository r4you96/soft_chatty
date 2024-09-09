from datetime import datetime
from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field

from app.domain import gen_id


class MessageBlockType(str, Enum):
    TEXT = 'TEXT'


class MessageBlockText(BaseModel):
    query: str


class MessageBlock(BaseModel):
    data_type: MessageBlockType
    data: Union[MessageBlockText]


class Message(BaseModel):
    id: str = Field(default_factory=gen_id)
    channel_id: str
    messaging_user_id: str
    user_name: str
    blocks: List[MessageBlock] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
