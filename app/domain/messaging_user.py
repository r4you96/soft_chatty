from datetime import datetime

from pydantic import BaseModel, Field

from app.domain import gen_id


class MessagingUser(BaseModel):
    id: str = Field(default_factory=gen_id)
    user_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
