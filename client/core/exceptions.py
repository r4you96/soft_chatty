from typing import Optional


class ClientException(Exception):
    status_code: int
    detail: Optional[str] = None

    def __init__(self,
                 status_code: int,
                 detail: Optional[str] = None):
        self.status_code = status_code
        self.detail = detail

