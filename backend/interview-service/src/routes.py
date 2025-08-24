"""
Interview 서비스 API 라우트
"""

from shared.utils.logger import setup_logger
import json
import asyncio
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse
from datetime import datetime

from src.crud import get_interview_by_unique_key
from src.service import generate_interview_questions_service
from tasks import get_task_progress_from_redis
from shared.celery_app import celery_app
from config import settings

logger = setup_logger("interview-service", settings.log_level)

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

# =================================
# 비동기 처리 API 엔드포인트들
# =================================

@router.post("/async/{unique_key}/questions", response_model=dict)
async def generate_interview_questions_async_api(unique_key: str):
    """
    비동기로 면접 질문 생성 시작
    즉시 task_id를 반환하고 백그라운드에서 처리
    
    Args:
        unique_key: 이력서 고유 키
        
    Returns:
        task_id: 작업 추적을 위한 고유 ID
        status: 작업 상태 (pending)
        estimated_time: 예상 완료 시간
    """
    try:
        # Celery 작업 시작 (full task name 사용)
        task = celery_app.send_task('tasks.generate_interview_questions_async', args=[unique_key], queue='interview_queue')
        
        logger.info(f"Async interview generation started for {unique_key}, task_id: {task.id}")
        
        return {
            "task_id": task.id,
            "status": "pending",
            "message": "면접 질문 생성 작업이 시작되었습니다",
            "unique_key": unique_key,
            "estimated_time": "30-60초",
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start async interview generation for {unique_key}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to start async interview generation: {str(e)}"
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
                    'message': '면접 질문 생성이 완료되었습니다!',
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
            # 에러 발생 시
            error_data = {
                'task_id': task_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            yield {
                "event": "error",
                "data": json.dumps(error_data)
            }
    
    # EventSource 응답 반환
    return EventSourceResponse(event_stream())