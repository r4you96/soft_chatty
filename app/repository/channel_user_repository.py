from datetime import datetime
from typing import Optional

from app.core.mongo import mongo
from app.domain.channel_user import ChannelUser


async def create(channel_user: ChannelUser):
    collection = mongo.db.channel_users
    await collection.insert_one(channel_user.model_dump(exclude_none=True))


async def read_by_messaging_user_id(channel_id: str, messaging_user_id: str) -> Optional[ChannelUser]:
    collection = mongo.db.channel_users
    query = {
        'channel_id': channel_id,
        'messaging_user_id': messaging_user_id
    }
    doc = await collection.find_one(query)

    return ChannelUser(**doc) if doc else None


async def update(data: ChannelUser):
    collection = mongo.db.channel_users
    data.updated_at = datetime.utcnow()
    data_for_update = data.model_dump(exclude={'id', 'created_at'})
    await collection.update_one({'id': data.id},
                                {'$set': data_for_update})


async def delete(channel_user_id: str):
    collection = mongo.db.channel_users
    query = {'id': channel_user_id}
    await collection.delete_one(query)
