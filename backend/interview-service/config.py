"""
Interview Service 설정
"""

from shared.config.base import BaseAppSettings

class InterviewServiceSettings(BaseAppSettings):
    """Interview Service 설정"""
    
    # Interview Service 전용 설정
    service_name: str = "interview"
    service_port: int = 8002
    api_prefix: str = "/api/v1/interview"
    
    # Interview 관련 설정
    max_questions_per_session: int = 5
    default_question_count: int = 5
    min_question_count: int = 3
    max_question_count: int = 8
    
    # API 설정 오버라이드
    api_host: str = "0.0.0.0"
    api_port: int = 8002  # Interview service 포트

settings = InterviewServiceSettings()