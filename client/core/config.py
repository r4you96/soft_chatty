import os
from os.path import exists
from pathlib import Path

from pydantic_settings import BaseSettings


PROFILE = os.environ.get("PROFILE", "local")


class Settings(BaseSettings):
    app_name: str
    socket_url: str

    class Config:
        file_path = f'{Path(os.path.dirname(__file__)).parent.parent}/config/client/{PROFILE}.env'
        # If we have an explicit env file, then use it. Otherwise, get from env variables.
        if exists(file_path):
            env_file = file_path
            env_file_encoding = 'utf-8'
        else:
            env_prefix = ""
        case_sensitive = False


config = Settings()
