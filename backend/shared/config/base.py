"""
모든 서비스의 기본 설정
"""

from pydantic_settings import BaseSettings

class BaseAppSettings(BaseSettings):
    """모든 서비스의 기본 설정"""
    
    # MongoDB 설정 (공통)
    mongodb_url: str = "mongodb://admin:password123@mongodb:27017/interview_coach?authSource=admin"
    database_name: str = "interview_coach"
    
    # 공통 설정
    log_level: str = "INFO"
    debug: bool = False
    
    # LLM 설정 (공통)
    openai_api_key: str = "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"
    openai_model: str = "gpt-4.1"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 4000  # 증가: 상세한 스키마를 위해
    openai_timeout: int = 60       # 증가: 복잡한 질문 생성을 위해
    
    # Claude 설정
    claude_api_key: str = "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"
    claude_model: str = "claude-sonnet-4-20250514"
    claude_temperature: float = 0.7
    claude_max_tokens: int = 4000  # 증가: 상세한 스키마를 위해
    claude_timeout: int = 60       # 증가: 복잡한 질문 생성을 위해
    
    # Gemini 설정 (무료 모델)
    gemini_api_key: str = "AIzaSyBNd4pC7QDcn54PH_AcKjCQCR_Jxi1QViM"
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.7
    gemini_max_tokens: int = 4000  # 증가: 상세한 스키마를 위해
    gemini_timeout: int = 60       # 증가: 복잡한 질문 생성을 위해
    
    class Config:
        env_file = ".env"   
        case_sensitive = False
