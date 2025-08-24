"""
Resume Service API 라우트 - Resume 관련 기능만 담당
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from urllib.parse import unquote
import re
from .schemas import ResumeCreate, ResumeResponse
from .crud import (
    create_resume as create_resume_db,
    get_resumes_by_name,
    get_resume_by_unique_key
)
from shared.utils.error_handler import ResumeErrors

router = APIRouter()

@router.get("/health")
async def health_check():
    """Resume 서비스 상태 확인"""
    return {
        "service": "resume-service", 
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

@router.post("/", response_model=dict)
async def create_resume(resume_data: ResumeCreate):
    """이력서 생성"""
    try:
        # 사용자별 이력서 개수 확인
        existing_count = await get_resumes_by_name(resume_data.name)
        next_count = len(existing_count) + 1
        
        # unique_key 생성: 사용자이름_순서
        unique_key = f"{resume_data.name}_{next_count}"
        
        # 이력서 데이터에 unique_key 추가
        resume_dict = resume_data.model_dump()
        resume_dict["unique_key"] = unique_key
        resume_dict["created_at"] = datetime.utcnow()
        resume_dict["updated_at"] = datetime.utcnow()
        
        # 데이터베이스에 저장
        resume_id = await create_resume_db(resume_dict)
        
        return {
            "message": "Resume created successfully",
            "resume_id": resume_id,
            "unique_key": unique_key
        }
        
    except Exception as e:
        raise ResumeErrors.creation_failed(str(e))

@router.get("/{unique_key}", response_model=ResumeResponse)
async def get_resume(unique_key: str):
    """unique_key로 이력서 조회"""
    try:
        resume = await get_resume_by_unique_key(unique_key)
        if not resume:
            raise ResumeErrors.not_found(unique_key)
        
        return ResumeResponse(**resume)
        
    except Exception as e:
        if hasattr(e, 'error_code'):  # APIError인 경우
            raise
        raise ResumeErrors.creation_failed(str(e))

@router.get("/user/{name}")
async def get_user_resumes(name: str):
    """사용자의 모든 이력서 조회"""
    try:
        # URL 디코딩
        decoded_name = unquote(name)
        
        # 입력 값 검증
        if not decoded_name or decoded_name.strip() == "":
            raise ResumeErrors.validation_error("name", "User name cannot be empty")
        
        # 이름 정리
        cleaned_name = decoded_name.strip()
        
        # 길이 검증
        if len(cleaned_name) > 100:
            raise ResumeErrors.validation_error("name", "User name is too long (max 100 characters)")
        
        # 최소 길이 검증
        if len(cleaned_name) < 1:
            raise ResumeErrors.validation_error("name", "User name is too short (min 1 character)")
        
        # 허용되지 않는 문자 검증 (예: 제어 문자, 특정 특수문자)
        if re.search(r'[\x00-\x1f\x7f-\x9f]', cleaned_name):  # 제어 문자
            raise ResumeErrors.validation_error("name", "User name contains invalid characters")
        
        resumes = await get_resumes_by_name(cleaned_name)
        
        # 강화된 에러 처리 옵션:
        # 1. 표준 REST API 방식: 빈 배열 반환 (일반적)
        # 2. 명확한 에러 처리: 404 에러 반환 (사용자 요청)
        
        # 사용자 요청에 따른 강화된 에러 처리 적용
        if not resumes or len(resumes) == 0:
            raise ResumeErrors.user_not_found(cleaned_name)
        
        return {
            "user": cleaned_name,
            "count": len(resumes),
            "resumes": resumes
        }
        
    except Exception as e:
        if hasattr(e, 'error_code'):  # APIError인 경우
            raise
        # 데이터베이스 조회 실패 등의 일반적인 에러
        raise ResumeErrors.retrieval_failed(name, str(e))

