from pydantic import BaseModel


class SocketParams(BaseModel):
    user_name: str


class SocketSession(BaseModel):
    user_name: str


# event models
class SocketChatEvent(BaseModel):
    query: str


# emit models
class SocketUserMessage(BaseModel):
    user_name: str
    query: str
