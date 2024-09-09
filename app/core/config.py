import os
from os.path import exists
from pathlib import Path

from pydantic_settings import BaseSettings


PROFILE = os.environ.get("PROFILE", "local")


class Settings(BaseSettings):
    app_name: str
    mongo_url: str
    mongo_database: str
    mongo_auth_source: str

    class Config:
        file_path = f'{Path(os.path.dirname(__file__)).parent.parent}/config/server/{PROFILE}.env'

        if exists(file_path):
            env_file = file_path
            env_file_encoding = 'utf-8'
        else:
            env_prefix = ""
        case_sensitive = False


config = Settings()
