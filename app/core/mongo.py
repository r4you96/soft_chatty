import sys
from typing import Optional, Any

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import AutoReconnect

from app.core.config import config
from app.core.logging import logger


class MongoDB:
    def __init__(self,
                 url: str,
                 database: str,
                 auth_source: str,
                 max_pool_size: int = 100,
                 min_pool_size: int = 0):
        self._url = url
        self._database = database
        self._auth_source = auth_source
        self._max_pool_size = max_pool_size
        self._min_pool_size = min_pool_size
        self.client: Optional[AsyncIOMotorClient] = None

    @property
    def db(self):
        if self.client:
            return self.client[self._database]
        else:
            return None

    async def connect(self):
        self.client = AsyncIOMotorClient(self._url,
                                         maxPoolSize=self._max_pool_size,
                                         minPoolSize=self._min_pool_size,
                                         serverSelectionTimeoutMS=5000,
                                         authSource=self._auth_source)
        try:
            await self.db.command('ping')
            print('ping')
        except AutoReconnect as e:
            self.client.close()
            logger.error(f'Could not connect to mongodb', exc_info=e)
            sys.exit(0)

    async def close(self):
        if self.client is not None:
            self.client.close()
            logger.info('Closed connection to mongoDB')


mongo = MongoDB(url=config.mongo_url,
                database=config.mongo_database,
                auth_source=config.mongo_auth_source)
