from datetime import datetime
from typing import Optional

from app.domain.channel_user import ChannelUserStatus, ChannelUser
from app.repository import channel_user_repository


async def open_channel(channel_id: str,
                       messaging_user_id: str,
                       previous_channel_id: Optional[str] = None):
    # close previous channel
    if previous_channel_id:
        channel_user = await channel_user_repository.read_by_messaging_user_id(
            channel_id=previous_channel_id,
            messaging_user_id=messaging_user_id
        )
        channel_user.status = ChannelUserStatus.CLOSE
        channel_user.closed_at = datetime.utcnow()
        await channel_user_repository.update(data=channel_user)

    # open next channel
    channel_user = await channel_user_repository.read_by_messaging_user_id(
        channel_id=channel_id,
        messaging_user_id=messaging_user_id
    )
    if channel_user:
        channel_user.status = ChannelUserStatus.OPEN
        channel_user.opened_at = datetime.utcnow()
        await channel_user_repository.update(data=channel_user)
    else:
        channel_user = ChannelUser(channel_id=channel_id,
                                   messaging_user_id=messaging_user_id,
                                   status=ChannelUserStatus.OPEN,
                                   opened_at=datetime.utcnow())
        await channel_user_repository.create(channel_user=channel_user)


async def close_channel(channel_id: str,
                        messaging_user_id: str):
    channel_user = await channel_user_repository.read_by_messaging_user_id(
        channel_id=channel_id,
        messaging_user_id=messaging_user_id
    )
    channel_user.status = ChannelUserStatus.CLOSE
    channel_user.closed_at = datetime.utcnow()
    await channel_user_repository.update(data=channel_user)
