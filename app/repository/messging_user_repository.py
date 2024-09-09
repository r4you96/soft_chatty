from typing import Optional

from app.core.mongo import mongo
from app.domain.messaging_user import MessagingUser


async def create(messaging_user: MessagingUser):
    collection = mongo.db.messaging_users
    await collection.insert_one(messaging_user.model_dump(exclude_none=True))


async def read_by_user_name(user_name: str) -> Optional[MessagingUser]:
    collection = mongo.db.messaging_users
    query = {
        'user_name': user_name
    }
    doc = await collection.find_one(query)

    return MessagingUser(**doc) if doc else None
