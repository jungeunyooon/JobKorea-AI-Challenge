"""
Resume Service API 라우트 - Resume 관련 기능만 담당
"""

from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from .schemas import ResumeCreate, ResumeResponse
from .crud import (
    create_resume as create_resume_db,
    get_resumes_by_name,
    get_resume_by_unique_key
)

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
        raise HTTPException(status_code=500, detail=f"Failed to create resume: {str(e)}")

@router.get("/{unique_key}", response_model=ResumeResponse)
async def get_resume(unique_key: str):
    """unique_key로 이력서 조회"""
    try:
        resume = await get_resume_by_unique_key(unique_key)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return ResumeResponse(**resume)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve resume: {str(e)}")

@router.get("/user/{name}")
async def get_user_resumes(name: str):
    """사용자의 모든 이력서 조회"""
    try:
        resumes = await get_resumes_by_name(name)
        return {
            "user": name,
            "count": len(resumes),
            "resumes": resumes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve resumes: {str(e)}")

