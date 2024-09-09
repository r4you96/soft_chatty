from app.domain.messaging_user import MessagingUser
from app.repository import messging_user_repository


async def get_or_create_user(user_name: str) -> MessagingUser:
    messaging_user = await messging_user_repository.read_by_user_name(user_name=user_name)
    if not messaging_user:
        messaging_user = MessagingUser(user_name=user_name)
        await messging_user_repository.create(messaging_user=messaging_user)
    return messaging_user
