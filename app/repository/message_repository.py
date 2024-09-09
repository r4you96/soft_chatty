from typing import List

from app.core.mongo import mongo
from app.domain.message import Message


async def create(message: Message):
    collection = mongo.db.messages
    data = message.model_dump()
    await collection.insert_one(data)


async def find(channel_id: str) -> List[Message]:
    collection = mongo.db.messages
    query = {'channel_id': channel_id}
    cursor = collection.find(query, sort=[('created_at', 1)])

    messages = [Message(**doc) async for doc in cursor]
    return messages
