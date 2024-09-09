from typing import Optional


class SocketClientStore:
    user_name: Optional[str] = None

    def __init__(self):
        pass

    def set_user_name(self, user_name: str):
        self.user_name = user_name


client_store = SocketClientStore()
