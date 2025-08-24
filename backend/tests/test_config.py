"""
테스트용 설정 클래스
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
from pathlib import Path
from dotenv import load_dotenv

# 테스트용 환경변수 파일 로드
test_env_path = Path(__file__).parent / "test.env"
load_dotenv(test_env_path, override=True)

class TestAppSettings(BaseSettings):
    """테스트용 애플리케이션 설정"""
    
    # MongoDB 설정
    mongodb_url: str = os.environ.get("MONGODB_URL", "mongodb://localhost:27017/interview_coach_test")
    database_name: str = os.environ.get("DATABASE_NAME", "interview_coach_test")
    
    # 공통 설정
    log_level: str = "DEBUG"
    debug: bool = True
    
    # LLM 설정 (테스트용 더미 값)
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "test-openai-key")
    openai_model: str = os.environ.get("OPENAI_MODEL", "gpt-4.1")
    openai_temperature: float = float(os.environ.get("OPENAI_TEMPERATURE", "0.7"))
    openai_max_tokens: int = int(os.environ.get("OPENAI_MAX_TOKENS", "1000"))
    openai_timeout: int = int(os.environ.get("OPENAI_TIMEOUT", "30"))
    
    # Claude 설정
    claude_api_key: str = os.environ.get("CLAUDE_API_KEY", "test-claude-key")
    claude_model: str = os.environ.get("CLAUDE_MODEL", "claude-3-haiku-20240307")
    claude_temperature: float = float(os.environ.get("CLAUDE_TEMPERATURE", "0.7"))
    claude_max_tokens: int = int(os.environ.get("CLAUDE_MAX_TOKENS", "1000"))
    claude_timeout: int = int(os.environ.get("CLAUDE_TIMEOUT", "30"))
    
    # Gemini 설정
    gemini_api_key: str = os.environ.get("GEMINI_API_KEY", "test-gemini-key")
    gemini_model: str = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    gemini_temperature: float = float(os.environ.get("GEMINI_TEMPERATURE", "0.7"))
    gemini_max_tokens: int = int(os.environ.get("GEMINI_MAX_TOKENS", "1000"))
    gemini_timeout: int = int(os.environ.get("GEMINI_TIMEOUT", "30"))
    
    # Celery 설정
    celery_broker_url: str = os.environ.get("CELERY_BROKER_URL", "amqp://localhost:5672//")
    celery_result_backend: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    celery_task_serializer: str = os.environ.get("CELERY_TASK_SERIALIZER", "json")
    celery_accept_content: str = os.environ.get("CELERY_ACCEPT_CONTENT", "json")
    celery_result_serializer: str = os.environ.get("CELERY_RESULT_SERIALIZER", "json")
    celery_timezone: str = os.environ.get("CELERY_TIMEZONE", "Asia/Seoul")
    
    # Redis 설정
    redis_host: str = os.environ.get("REDIS_HOST", "localhost")
    redis_port: int = int(os.environ.get("REDIS_PORT", "6379"))
    
    model_config = ConfigDict(
        env_file="test.env",
        case_sensitive=False,
        extra="ignore"  # 추가 필드 무시
    )
