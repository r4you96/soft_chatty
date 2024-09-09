from datetime import datetime, timedelta
from typing import List, Optional

from app.core.mongo import mongo
from app.domain.channel import Channel, ChannelForClient


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


async def find_channel_for_client() -> List[ChannelForClient]:
    collection = mongo.db.channels

    thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
    channel_user_lookup = {
        'from': 'channel_users',
        'let': {'channel_id': '$id'},
        'pipeline': [
            {'$match': {
                '$expr': {'$eq': ['$channel_id', '$$channel_id']},
                '$or': [
                    {'closed_at': {'$gte': thirty_minutes_ago}},
                    {'status': 'OPEN'}
                ]
            }}
        ],
        'as': 'channel_users'
    }
    message_lookup = {
        'from': 'messages',
        'let': {'channel_id': '$id'},
        'pipeline': [
            {'$match': {
                '$expr': {'$eq': ['$channel_id', '$$channel_id']},
            }},
            {'$sort': {'created_at': -1}},
            {'$limit': 1}
        ],
        'as': 'messages'
    }
    pipeline = [
        {'$lookup': channel_user_lookup},
        {'$addFields': {'active_count': {'$size': '$channel_users'}}},
        {'$lookup': message_lookup},
        {'$addFields': {'last_message': {'$arrayElemAt': ['$messages', 0]}}},
        {'$sort': {'active_count': -1}}
    ]

    cursor = collection.aggregate(pipeline=pipeline)
    channels = [ChannelForClient(**channel) async for channel in cursor]

    return channels
