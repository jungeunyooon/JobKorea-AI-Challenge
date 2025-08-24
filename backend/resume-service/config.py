"""
Resume Service 설정
"""

from shared.config.base import BaseAppSettings

class ResumeServiceSettings(BaseAppSettings):
    """Resume Service 설정"""
    
    # Resume Service 전용 설정
    service_name: str = "resume"
    service_port: int = 8001
    api_prefix: str = "/api/v1/resumes"
    
    # Resume 관련 설정
    max_resumes_per_user: int = 10
    unique_key_format: str = "{name}_{count}"
    
    # API 설정 오버라이드
    api_host: str = "0.0.0.0"
    api_port: int = 8001  # Resume service 포트

settings = ResumeServiceSettings()