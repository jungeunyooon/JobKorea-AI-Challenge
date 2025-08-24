"""
MongoDB 연결 관리
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from typing import Optional
import logging
from shared.config.base import BaseAppSettings

logger = logging.getLogger(__name__)

# Celery tasks용 동기 연결
def get_database():
    """
    Celery tasks용 동기 MongoDB 연결
    """
    settings = BaseAppSettings()
    try:
        client = pymongo.MongoClient(settings.mongodb_url)
        database = client[settings.database_name]
        return database
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

class DatabaseManager:
    """MongoDB 연결 관리자"""
    
    def __init__(self, mongodb_url: str, database_name: str):
        self.mongodb_url = mongodb_url
        self.database_name = database_name
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self):
        """MongoDB 연결"""
        try:
            self.client = AsyncIOMotorClient(self.mongodb_url)
            self.database = self.client[self.database_name]
            logger.info(f"Connected to MongoDB: {self.database_name}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """MongoDB 연결 종료"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def get_collection(self, collection_name: str):
        """컬렉션 반환"""
        if self.database is None:
            raise RuntimeError("Database not connected")
        return self.database[collection_name]
    
    async def ping(self) -> bool:
        """연결 상태 확인"""
        try:
            if self.database is not None:
                await self.database.command("ping")
                return True
        except Exception as e:
            logger.error(f"Database ping failed: {e}")
        return False
