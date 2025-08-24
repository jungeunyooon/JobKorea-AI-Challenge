"""
Interview 서비스 API 라우트
"""

import logging
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from src.crud import get_interview_by_unique_key, create_interview_questions
from src.service import generate_interview_questions_service
from src.schemas import InterviewQuestionsResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/{unique_key}/questions", response_model=dict)
async def generate_interview_questions(unique_key: str):
    """unique_key를 기반으로 면접 질문 생성 (여러 번 생성 가능)
    
    Args:
        unique_key: 이력서 고유 키
    
    Note:
        기본 LLM: Gemini (폴백: Gemini -> OpenAI -> Claude)
    """
    # Gemini 고정 사용
    provider = "gemini"
    
    try:
        logger.error(f"Routes: About to call generate_interview_questions_service with {unique_key}, {provider}")
        # 면접 질문 생성 및 저장
        result = await generate_interview_questions_service(unique_key, provider)
        logger.error(f"Routes: Service call completed successfully")
        
        return {
            "interview_id": str(result["interview_id"]),
            "resume_id": str(result["resume_id"]),
            "unique_key": unique_key,
            "provider": provider,
            "model": result.get("model", "unknown"),
            "questions": result["questions"],
            "generated_at": result["generated_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate interview questions: {str(e)}")

@router.get("/{unique_key}/questions", response_model=dict)
async def get_interview_questions(unique_key: str):
    """unique_key로 면접 질문 조회"""
    try:
        # 면접 질문들 조회
        interview = await get_interview_by_unique_key(unique_key)
        
        if not interview:
            raise HTTPException(status_code=404, detail="No interview questions found for this resume")
        
        return {
            "unique_key": interview["unique_key"],
            "questions": interview["questions"],
            "created_at": interview["created_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve interview questions: {str(e)}")

@router.get("/health")
async def health_check():
    """Interview 서비스 상태 확인"""
    return {
        "service": "interview-service",
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

@router.get("/debug/llm-fallback")
async def debug_llm_fallback():
    """LLM Registry fallback 테스트"""
    from shared.llm.registry import registry
    
    try:
        # get_client_with_fallback 직접 테스트
        client = registry.get_client_with_fallback()
        
        return {
            "fallback_client": client.name if client else None,
            "client_exists": client is not None
        }
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/debug/llm")
async def debug_llm():
    """LLM Registry 디버깅"""
    from shared.llm.registry import registry
    
    try:
        available_clients = registry.get_available_clients()
        
        # 각 클라이언트 생성 테스트
        client_status = {}
        for client_name in ["openai", "claude", "gemini"]:
            try:
                client = registry.get_client(client_name)
                client_status[client_name] = {
                    "available": client_name in available_clients,
                    "created": client is not None,
                    "name": client.name if client else None
                }
            except Exception as e:
                client_status[client_name] = {
                    "available": client_name in available_clients,
                    "created": False,
                    "error": str(e)
                }
        
        return {
            "available_clients": available_clients,
            "client_status": client_status
        }
        
    except Exception as e:
        return {"error": str(e)}