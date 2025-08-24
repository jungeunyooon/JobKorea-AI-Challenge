"""
모든 서비스의 기본 설정
"""

from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAppSettings(BaseSettings):
    """모든 서비스의 기본 설정"""
    
    # MongoDB 설정 (공통)
    mongodb_url: str = os.environ.get("MONGODB_URL")
    database_name: str = os.environ.get("DATABASE_NAME")
    
    # 공통 설정
    log_level: str = "INFO"
    debug: bool = False
    
    # LLM 설정 (공통)
    openai_api_key: str = os.environ.get("OPENAI_API_KEY")
    openai_model: str = os.environ.get("OPENAI_MODEL")
    openai_temperature: float = os.environ.get("OPENAI_TEMPERATURE")
    openai_max_tokens: int = os.environ.get("OPENAI_MAX_TOKENS")
    openai_timeout: int = os.environ.get("OPENAI_TIMEOUT")
    
    # Claude 설정
    claude_api_key: str = os.environ.get("CLAUDE_API_KEY")
    claude_model: str = os.environ.get("CLAUDE_MODEL")
    claude_temperature: float = os.environ.get("CLAUDE_TEMPERATURE")
    claude_max_tokens: int = os.environ.get("CLAUDE_MAX_TOKENS")
    claude_timeout: int = os.environ.get("CLAUDE_TIMEOUT")
    
    # Gemini 설정 (무료 모델)
    gemini_api_key: str = os.environ.get("GEMINI_API_KEY")
    gemini_model: str = os.environ.get("GEMINI_MODEL")
    gemini_temperature: float = os.environ.get("GEMINI_TEMPERATURE")
    gemini_max_tokens: int = os.environ.get("GEMINI_MAX_TOKENS")
    gemini_timeout: int = os.environ.get("GEMINI_TIMEOUT")
    
    class Config:
        env_file = ".env"   
        case_sensitive = False
