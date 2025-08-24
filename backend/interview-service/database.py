"""
Interview Service 데이터베이스 설정
"""

from shared.database.connection import DatabaseManager
from shared.database.collections import Collections
from shared.utils.logger import setup_logger
from config import settings

logger = setup_logger("interview-service", settings.log_level)

# Interview Service 전용 데이터베이스 매니저
db_manager = DatabaseManager(settings.mongodb_url, settings.database_name)

async def connect_to_mongo():
    """MongoDB 연결"""
    await db_manager.connect()
    logger.info("Interview Service connected to MongoDB")

async def close_mongo_connection():
    """MongoDB 연결 종료"""
    await db_manager.disconnect()
    logger.info("Interview Service disconnected from MongoDB")

def get_database():
    """데이터베이스 반환"""
    return db_manager.database

def get_interview_collection():
    """Interview 컬렉션 반환"""
    return db_manager.get_collection(Collections.INTERVIEW_QUESTIONS)

def get_resumes_collection():
    """Resume 컬렉션 반환 (다른 서비스 데이터 접근)"""
    return db_manager.get_collection(Collections.RESUMES)