"""
Learning Service API 라우트
"""

from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from .service import generate_learning_path_service
from .schemas import LearningPathCreateResponse, LearningPathRequest
from database import get_learning_collection

router = APIRouter()

@router.post("/{unique_key}/learning-path", response_model=LearningPathCreateResponse)
async def generate_learning_path(unique_key: str):
    """특정 unique_key의 이력서를 기반으로 학습 경로 생성 (여러 번 생성 가능)
    
    Args:
        unique_key: 이력서 고유 키
    
    Note:
        기본 LLM: Gemini (폴백: Gemini -> OpenAI -> Claude)
    """
    # Gemini 고정 사용
    provider = "gemini"
    
    try:
        # 학습 경로 생성
        result = await generate_learning_path_service(unique_key, provider)
        
        return {
            "message": "Learning path generated successfully",
            "unique_key": unique_key,
            "provider": provider,
            "model": result.get("model", "unknown"),  # 사용된 모델 정보 포함
            "analysis": result.get("analysis", {"strengths": [], "weaknesses": []}),
            "summary": result["summary"],
            "learning_paths": result["learning_paths"],
            "generated_at": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate learning path: {str(e)}")

@router.get("/{unique_key}/learning-path", response_model=dict)
async def get_learning_path(unique_key: str):
    """unique_key로 학습 경로 조회"""
    try:
        # 학습 경로들 조회 (최신 순으로 정렬)
        learning_collection = get_learning_collection()
        learning_paths = await learning_collection.find(
            {"unique_key": unique_key}
        ).sort("created_at", -1).to_list(length=10)  # 최근 10개까지
        
        if not learning_paths:
            raise HTTPException(
                status_code=404, 
                detail="No learning paths found for this resume"
            )
        
        # 가장 최근 것을 기본으로 반환
        latest = learning_paths[0]
        
        return {
            "unique_key": latest["unique_key"],
            "provider": latest.get("provider", "unknown"),
            "model": latest.get("model", "unknown"),
            "analysis": latest.get("analysis", {"strengths": [], "weaknesses": []}),
            "summary": latest["summary"],
            "learning_paths": latest["learning_paths"],
            "created_at": latest["created_at"],
            "total_generated": len(learning_paths)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve learning paths: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Learning 서비스 상태 확인"""
    return {
        "service": "learning-service",
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

@router.get("/debug/llm")
async def debug_llm():
    """LLM Registry 디버깅 (Learning Service용)"""
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
            "service": "learning-service",
            "available_clients": available_clients,
            "client_status": client_status
        }
        
    except Exception as e:
        return {"service": "learning-service", "error": str(e)}
