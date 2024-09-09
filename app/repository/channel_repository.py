from typing import List, Optional

from app.core.mongo import mongo
from app.domain.channel import Channel


async def create(channel: Channel):
    collection = mongo.db.channels
    await collection.insert_one(channel.model_dump(exclude_none=True))


async def read_by_name(channel_name: str) -> Optional[Channel]:
    collection = mongo.db.channels
    query = {'name': channel_name}
    doc = await collection.find_one(query)

    return Channel(**doc) if doc else None


async def find_channel() -> List[Channel]:
    collection = mongo.db.channels
    cursor = collection.find()
    channels = [Channel(**doc) async for doc in cursor]

    return channels
