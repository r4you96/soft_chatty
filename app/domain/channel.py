from datetime import datetime

from pydantic import BaseModel, Field

from app.domain import gen_id


class Channel(BaseModel):
    id: str = Field(default_factory=gen_id)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChannelCreate(BaseModel):
    name: str
