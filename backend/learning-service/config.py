"""
Learning Service 설정
"""

from shared.config.base import BaseAppSettings

class LearningServiceSettings(BaseAppSettings):
    """Learning Service 설정"""
    
    # Learning Service 전용 설정
    service_name: str = "learning"
    service_port: int = 8003
    api_prefix: str = "/api/v1/learning"
    
    # Learning Path 관련 설정
    max_learning_paths_per_session: int = 8
    min_learning_paths: int = 3
    default_learning_paths_count: int = 6
    
    # API 설정 오버라이드
    api_host: str = "0.0.0.0"
    api_port: int = 8003  # Learning service 포트

settings = LearningServiceSettings()