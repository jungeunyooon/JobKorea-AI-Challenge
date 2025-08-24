"""
Learning Service API 라우트
"""

import logging
import json
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from typing import List, Dict, Any
from datetime import datetime
from celery.result import AsyncResult

from .service import generate_learning_path_service
from .schemas import LearningPathCreateResponse, LearningPathRequest
from database import get_learning_collection
from tasks import generate_learning_path_async, get_task_progress_from_redis
from shared.celery_app import celery_app

logger = logging.getLogger(__name__)

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


# =================================
# 비동기 처리 API 엔드포인트들
# =================================

@router.post("/async/{unique_key}/learning-path", response_model=dict)
async def generate_learning_path_async_api(unique_key: str):
    """
    비동기로 학습 경로 생성 시작
    즉시 task_id를 반환하고 백그라운드에서 처리
    """
    try:
        # Celery 작업 시작 (full task name 사용)
        task = celery_app.send_task('learning_service.tasks.generate_learning_path_async', args=[unique_key], queue='learning_queue')
        logger.info(f"Async learning path generation started for {unique_key}, task_id: {task.id}")
        return {
            "task_id": task.id,
            "status": "pending",
            "message": "학습 경로 생성 작업이 시작되었습니다",
            "unique_key": unique_key,
            "estimated_time": "30-60초",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to start async learning path generation for {unique_key}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start async learning path generation: {str(e)}"
        )

@router.get("/tasks/{task_id}/progress", response_model=dict)
async def get_task_progress_api(task_id: str):
    """
    작업 진행 상황 조회 (Redis 기반)
    
    Args:
        task_id: 작업 고유 ID
        
    Returns:
        task_id: 작업 ID
        state: 작업 상태 (PENDING, PROGRESS, SUCCESS, FAILURE)
        progress: 진행률 (0-100)
        message: 현재 단계 메시지
        result: 완료된 경우 결과 데이터
    """
    try:
        return get_task_progress_from_redis(task_id)
    except Exception as e:
        logger.error(f"Failed to get task progress for {task_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get task progress: {str(e)}"
        )

@router.get("/tasks/{task_id}/stream")
async def stream_task_progress(task_id: str):
    """
    SSE로 작업 진행 상황 실시간 스트리밍
    
    Args:
        task_id: 작업 고유 ID
        
    Returns:
        SSE 스트림 (Server-Sent Events)
    """
    
    async def event_stream():
        """SSE 이벤트 스트림 생성기"""
        try:
            last_progress = -1
            
            # 작업이 완료될 때까지 반복
            while True:
                # Redis에서 진행 상황 조회
                progress_data = get_task_progress_from_redis(task_id)
                
                # 완료되었거나 실패했으면 종료
                if progress_data.get('state') in ['SUCCESS', 'FAILURE']:
                    break
                
                # 진행률이 변경된 경우만 이벤트 전송
                current_progress = progress_data.get('progress', 0)
                if current_progress != last_progress:
                    yield {
                        "event": "progress",
                        "data": json.dumps(progress_data)
                    }
                    last_progress = current_progress
                
                # 1초 대기
                await asyncio.sleep(1)
            
            # 최종 결과 전송 (Redis에서 가져온 데이터 사용)
            if progress_data.get('state') == 'SUCCESS':
                final_data = {
                    'task_id': task_id,
                    'state': 'SUCCESS',
                    'progress': 100,
                    'message': '학습 경로 생성이 완료되었습니다!',
                    'stage': 'completed',
                    'result': progress_data.get('result'),
                    'timestamp': datetime.now().isoformat()
                }
                
                yield {
                    "event": "completed",
                    "data": json.dumps(final_data)
                }
            else:  # FAILURE
                error_data = {
                    'task_id': task_id,
                    'state': 'FAILURE',
                    'progress': 0,
                    'message': progress_data.get('message', '오류가 발생했습니다'),
                    'stage': 'failed',
                    'error': progress_data.get('error', '알 수 없는 오류'),
                    'timestamp': datetime.now().isoformat()
                }
                
                yield {
                    "event": "error",
                    "data": json.dumps(error_data)
                }
            
            # 스트림 종료 신호
            yield {
                "event": "close",
                "data": json.dumps({
                    "message": "Stream completed",
                    "timestamp": datetime.now().isoformat()
                })
            }

        except Exception as e:
            error_data = {
                'task_id': task_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            yield {
                "event": "error",
                "data": json.dumps(error_data)
            }

    return EventSourceResponse(event_stream())
