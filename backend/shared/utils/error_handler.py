"""
공통 에러 처리 유틸리티
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class ErrorCode(Enum):
    """표준 에러 코드"""
    
    # Resume Service Errors (1000-1999)
    RESUME_NOT_FOUND = "RESUME_NOT_FOUND"
    RESUME_CREATION_FAILED = "RESUME_CREATION_FAILED"
    RESUME_VALIDATION_ERROR = "RESUME_VALIDATION_ERROR"
    RESUME_UPDATE_FAILED = "RESUME_UPDATE_FAILED"
    RESUME_DELETE_FAILED = "RESUME_DELETE_FAILED"
    
    # Interview Service Errors (2000-2999)
    INTERVIEW_GENERATION_FAILED = "INTERVIEW_GENERATION_FAILED"
    INTERVIEW_NOT_FOUND = "INTERVIEW_NOT_FOUND"
    INTERVIEW_TASK_FAILED = "INTERVIEW_TASK_FAILED"
    INTERVIEW_LLM_ERROR = "INTERVIEW_LLM_ERROR"
    
    # Learning Service Errors (3000-3999)
    LEARNING_PATH_GENERATION_FAILED = "LEARNING_PATH_GENERATION_FAILED"
    LEARNING_PATH_NOT_FOUND = "LEARNING_PATH_NOT_FOUND"
    LEARNING_TASK_FAILED = "LEARNING_TASK_FAILED"
    LEARNING_LLM_ERROR = "LEARNING_LLM_ERROR"
    
    # LLM Service Errors (4000-4999)
    LLM_PROVIDER_NOT_AVAILABLE = "LLM_PROVIDER_NOT_AVAILABLE"
    LLM_API_RATE_LIMIT = "LLM_API_RATE_LIMIT"
    LLM_API_TIMEOUT = "LLM_API_TIMEOUT"
    LLM_RESPONSE_PARSING_ERROR = "LLM_RESPONSE_PARSING_ERROR"
    LLM_INVALID_RESPONSE = "LLM_INVALID_RESPONSE"
    
    # Database Errors (5000-5999)
    DATABASE_CONNECTION_ERROR = "DATABASE_CONNECTION_ERROR"
    DATABASE_OPERATION_FAILED = "DATABASE_OPERATION_FAILED"
    DATABASE_TIMEOUT = "DATABASE_TIMEOUT"
    
    # Celery/Queue Errors (6000-6999)
    TASK_QUEUE_ERROR = "TASK_QUEUE_ERROR"
    TASK_EXECUTION_FAILED = "TASK_EXECUTION_FAILED"
    TASK_TIMEOUT = "TASK_TIMEOUT"
    TASK_RETRY_EXHAUSTED = "TASK_RETRY_EXHAUSTED"
    
    # General Errors (9000-9999)
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"


class APIError(Exception):
    """표준 API 에러 클래스"""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


def create_error_response(
    message: str,
    error_code: ErrorCode,
    status_code: int = 500,
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> Dict[str, Any]:
    """표준 에러 응답 생성"""
    
    error_response = {
        "detail": message,
        "error_code": error_code.value,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if details:
        error_response["details"] = details
        
    if request_id:
        error_response["request_id"] = request_id
        
    return error_response


async def handle_api_error(request: Request, exc: APIError) -> JSONResponse:
    """API 에러 핸들러"""
    
    error_response = create_error_response(
        message=exc.message,
        error_code=exc.error_code,
        status_code=exc.status_code,
        details=exc.details,
        request_id=getattr(request.state, 'request_id', None)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP 예외 핸들러"""
    
    # 기존 HTTPException을 표준 형식으로 변환
    error_code = _map_status_code_to_error_code(exc.status_code)
    
    error_response = create_error_response(
        message=str(exc.detail),
        error_code=error_code,
        status_code=exc.status_code,
        request_id=getattr(request.state, 'request_id', None)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
    """Validation 에러 핸들러"""
    
    error_response = create_error_response(
        message="Request validation failed",
        error_code=ErrorCode.VALIDATION_ERROR,
        status_code=422,
        details={"validation_errors": str(exc)},
        request_id=getattr(request.state, 'request_id', None)
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response
    )


async def handle_general_exception(request: Request, exc: Exception) -> JSONResponse:
    """일반 예외 핸들러"""
    
    error_response = create_error_response(
        message="An unexpected error occurred",
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        status_code=500,
        details={"exception_type": type(exc).__name__},
        request_id=getattr(request.state, 'request_id', None)
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response
    )


def _map_status_code_to_error_code(status_code: int) -> ErrorCode:
    """HTTP 상태 코드를 에러 코드로 매핑"""
    
    mapping = {
        400: ErrorCode.BAD_REQUEST,
        401: ErrorCode.UNAUTHORIZED,
        403: ErrorCode.FORBIDDEN,
        404: ErrorCode.RESUME_NOT_FOUND,  # 기본값
        422: ErrorCode.VALIDATION_ERROR,
        500: ErrorCode.INTERNAL_SERVER_ERROR,
        503: ErrorCode.SERVICE_UNAVAILABLE
    }
    
    return mapping.get(status_code, ErrorCode.INTERNAL_SERVER_ERROR)


# 서비스별 편의 함수들
class ResumeErrors:
    """Resume 서비스 에러 생성 함수들"""
    
    @staticmethod
    def not_found(unique_key: str) -> APIError:
        return APIError(
            message=f"Resume not found with key: {unique_key}",
            error_code=ErrorCode.RESUME_NOT_FOUND,
            status_code=404,
            details={"unique_key": unique_key}
        )
    
    @staticmethod
    def creation_failed(reason: str) -> APIError:
        return APIError(
            message=f"Failed to create resume: {reason}",
            error_code=ErrorCode.RESUME_CREATION_FAILED,
            status_code=500,
            details={"reason": reason}
        )
    
    @staticmethod
    def validation_error(field: str, message: str) -> APIError:
        return APIError(
            message=f"Validation error in field '{field}': {message}",
            error_code=ErrorCode.RESUME_VALIDATION_ERROR,
            status_code=422,
            details={"field": field, "validation_message": message}
        )
    
    @staticmethod
    def user_not_found(user_name: str) -> APIError:
        return APIError(
            message=f"No resumes found for user: {user_name}",
            error_code=ErrorCode.RESUME_NOT_FOUND,
            status_code=404,
            details={"user_name": user_name, "reason": "user_not_found"}
        )
    
    @staticmethod
    def retrieval_failed(user_name: str, reason: str) -> APIError:
        return APIError(
            message=f"Failed to retrieve resumes for user '{user_name}': {reason}",
            error_code=ErrorCode.DATABASE_OPERATION_FAILED,
            status_code=500,
            details={"user_name": user_name, "reason": reason}
        )


class InterviewErrors:
    """Interview 서비스 에러 생성 함수들"""
    
    @staticmethod
    def not_found(unique_key: str) -> APIError:
        return APIError(
            message=f"No interview questions found for resume: {unique_key}",
            error_code=ErrorCode.INTERVIEW_NOT_FOUND,
            status_code=404,
            details={"unique_key": unique_key}
        )
    
    @staticmethod
    def generation_failed(unique_key: str, reason: str) -> APIError:
        return APIError(
            message=f"Failed to generate interview questions for {unique_key}: {reason}",
            error_code=ErrorCode.INTERVIEW_GENERATION_FAILED,
            status_code=500,
            details={"unique_key": unique_key, "reason": reason}
        )
    
    @staticmethod
    def validation_error(field: str, message: str) -> APIError:
        return APIError(
            message=f"Validation error in field '{field}': {message}",
            error_code=ErrorCode.INTERVIEW_VALIDATION_ERROR,
            status_code=422,
            details={"field": field, "validation_message": message}
        )
    
    @staticmethod
    def retrieval_failed(unique_key: str, reason: str) -> APIError:
        return APIError(
            message=f"Failed to retrieve interview questions for {unique_key}: {reason}",
            error_code=ErrorCode.DATABASE_OPERATION_FAILED,
            status_code=500,
            details={"unique_key": unique_key, "reason": reason}
        )
    
    @staticmethod
    def llm_error(provider: str, error_message: str) -> APIError:
        return APIError(
            message=f"LLM provider '{provider}' error: {error_message}",
            error_code=ErrorCode.INTERVIEW_LLM_ERROR,
            status_code=503,
            details={"provider": provider, "llm_error": error_message}
        )
    
    @staticmethod
    def task_failed(task_id: str, reason: str) -> APIError:
        return APIError(
            message=f"Interview task {task_id} failed: {reason}",
            error_code=ErrorCode.INTERVIEW_TASK_FAILED,
            status_code=500,
            details={"task_id": task_id, "reason": reason}
        )


class LearningErrors:
    """Learning 서비스 에러 생성 함수들"""
    
    @staticmethod
    def not_found(unique_key: str) -> APIError:
        return APIError(
            message=f"No learning paths found for resume: {unique_key}",
            error_code=ErrorCode.LEARNING_NOT_FOUND,
            status_code=404,
            details={"unique_key": unique_key}
        )
    
    @staticmethod
    def generation_failed(unique_key: str, reason: str) -> APIError:
        return APIError(
            message=f"Failed to generate learning path for {unique_key}: {reason}",
            error_code=ErrorCode.LEARNING_PATH_GENERATION_FAILED,
            status_code=500,
            details={"unique_key": unique_key, "reason": reason}
        )
    
    @staticmethod
    def validation_error(field: str, message: str) -> APIError:
        return APIError(
            message=f"Validation error in field '{field}': {message}",
            error_code=ErrorCode.LEARNING_VALIDATION_ERROR,
            status_code=422,
            details={"field": field, "validation_message": message}
        )
    
    @staticmethod
    def retrieval_failed(unique_key: str, reason: str) -> APIError:
        return APIError(
            message=f"Failed to retrieve learning paths for {unique_key}: {reason}",
            error_code=ErrorCode.DATABASE_OPERATION_FAILED,
            status_code=500,
            details={"unique_key": unique_key, "reason": reason}
        )
    
    @staticmethod
    def llm_error(provider: str, error_message: str) -> APIError:
        return APIError(
            message=f"LLM provider '{provider}' error: {error_message}",
            error_code=ErrorCode.LEARNING_LLM_ERROR,
            status_code=503,
            details={"provider": provider, "llm_error": error_message}
        )


class LLMErrors:
    """LLM 관련 에러 생성 함수들"""
    
    @staticmethod
    def provider_not_available(provider: str) -> APIError:
        return APIError(
            message=f"LLM provider '{provider}' is not available",
            error_code=ErrorCode.LLM_PROVIDER_NOT_AVAILABLE,
            status_code=503,
            details={"provider": provider}
        )
    
    @staticmethod
    def response_parsing_error(provider: str, raw_response: str) -> APIError:
        return APIError(
            message=f"Failed to parse response from '{provider}'",
            error_code=ErrorCode.LLM_RESPONSE_PARSING_ERROR,
            status_code=500,
            details={
                "provider": provider,
                "raw_response_length": len(raw_response),
                "raw_response_preview": raw_response[:200] if raw_response else None
            }
        )
    
    @staticmethod
    def api_timeout(provider: str, timeout_seconds: int) -> APIError:
        return APIError(
            message=f"Timeout calling '{provider}' API after {timeout_seconds} seconds",
            error_code=ErrorCode.LLM_API_TIMEOUT,
            status_code=504,
            details={"provider": provider, "timeout_seconds": timeout_seconds}
        )
    
    @staticmethod
    def rate_limit_exceeded(provider: str) -> APIError:
        return APIError(
            message=f"Rate limit exceeded for '{provider}' API",
            error_code=ErrorCode.LLM_API_RATE_LIMIT,
            status_code=429,
            details={"provider": provider}
        )


class CeleryErrors:
    """Celery 관련 에러 생성 함수들"""
    
    @staticmethod
    def task_execution_failed(task_name: str, task_id: str, reason: str) -> APIError:
        return APIError(
            message=f"Task '{task_name}' execution failed: {reason}",
            error_code=ErrorCode.TASK_EXECUTION_FAILED,
            status_code=500,
            details={"task_name": task_name, "task_id": task_id, "reason": reason}
        )
    
    @staticmethod
    def queue_error(queue_name: str, reason: str) -> APIError:
        return APIError(
            message=f"Queue '{queue_name}' error: {reason}",
            error_code=ErrorCode.TASK_QUEUE_ERROR,
            status_code=503,
            details={"queue_name": queue_name, "reason": reason}
        )
