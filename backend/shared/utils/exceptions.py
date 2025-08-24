"""
공통 예외 클래스
"""

class BaseServiceException(Exception):
    """서비스 기본 예외"""
    def __init__(self, message: str, service_name: str = "unknown"):
        self.message = message
        self.service_name = service_name
        super().__init__(self.message)

class DatabaseConnectionError(BaseServiceException):
    """데이터베이스 연결 오류"""
    pass

class LLMServiceError(BaseServiceException):
    """LLM 서비스 오류"""
    pass

class ValidationError(BaseServiceException):
    """유효성 검증 오류"""
    pass

class NotFoundError(BaseServiceException):
    """리소스를 찾을 수 없음"""
    pass
