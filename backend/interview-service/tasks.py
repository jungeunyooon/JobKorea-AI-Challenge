"""
Interview Service Celery Tasks
진행률 추적과 함께 면접 질문 생성 작업 처리
"""

import logging
import json
import redis
from typing import Dict, Any
from datetime import datetime
from celery import current_task, current_app
from shared.config.base import BaseAppSettings
from shared.database.connection import get_database
from shared.utils.resume_formatter import format_resume_for_interview
from shared.utils.json_parser import parse_llm_json_response
from shared.llm.registry import registry
from shared.prompts.loader import get_prompt_loader

logger = logging.getLogger(__name__)
settings = BaseAppSettings()

# Redis 직접 연결 (progress tracking용)
redis_client = redis.from_url("redis://redis:6379/0")

def set_task_progress(task_id: str, progress_data: Dict[str, Any]):
    """Redis에 직접 task progress 저장"""
    try:
        key = f"task_progress:{task_id}"
        redis_client.setex(key, 3600, json.dumps(progress_data))  # 1시간 TTL
        logger.info(f"Progress saved for task {task_id}: {progress_data.get('progress', 0)}%")
    except Exception as e:
        logger.error(f"Failed to save progress for task {task_id}: {e}")

def get_task_progress_from_redis(task_id: str) -> Dict[str, Any]:
    """Redis에서 직접 task progress 조회"""
    try:
        key = f"task_progress:{task_id}"
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return {
            'task_id': task_id,
            'state': 'PENDING',
            'progress': 0,
            'message': '작업 대기 중...',
            'stage': 'pending'
        }
    except Exception as e:
        logger.error(f"Failed to get progress for task {task_id}: {e}")
        return {
            'task_id': task_id,
            'state': 'ERROR',
            'progress': 0,
            'message': f'진행률 조회 오류: {str(e)}',
            'stage': 'error'
        }

@current_app.task(bind=True, name='tasks.generate_interview_questions_async')
def generate_interview_questions_async(self, resume_id: str) -> Dict[str, Any]:
    """
    비동기로 면접 질문 생성
    진행률 업데이트와 함께 처리
    """
    try:
        # 1. 이력서 데이터 로드 (10%)
        set_task_progress(self.request.id, {
            'state': 'PROGRESS',
            'progress': 10,
            'message': '이력서 데이터를 불러오고 있습니다...',
            'stage': 'loading_resume',
            'timestamp': datetime.now().isoformat()
        })
        
        # MongoDB 연결 및 이력서 조회
        db = get_database()
        resume_collection = db.resumes
        resume_data = resume_collection.find_one({"unique_key": resume_id})
        
        if not resume_data:
            raise ValueError(f"Resume not found: {resume_id}")
        
        logger.info(f"Resume data retrieved for {resume_id}")
        
        # 2. 프롬프트 생성 (30%)
        set_task_progress(self.request.id, {
            'state': 'PROGRESS',
            'progress': 30,
            'message': '개인 맞춤형 프롬프트를 생성하고 있습니다...',
            'stage': 'generating_prompt',
            'timestamp': datetime.now().isoformat()
        })
        
        # 이력서 데이터 포맷팅
        formatted_data = format_resume_for_interview(resume_data)
        
        # 프롬프트 로드 및 렌더링
        loader = get_prompt_loader('interview')
        config = loader.load_prompt_config('interview_questions.yaml')
        
        # 시스템 및 휴먼 프롬프트 렌더링
        system_prompt = loader.render_system_prompt(config)
        human_prompt = loader.render_human_prompt(config, formatted_data)
        
        prompt_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ]
        
        logger.info(f"Prompt generated for {resume_id}")
        
        # 3. LLM API 호출 (70%)
        set_task_progress(self.request.id, {
            'state': 'PROGRESS',
            'progress': 70,
            'message': 'AI가 면접 질문을 생성하고 있습니다... (최대 30초 소요)',
            'stage': 'calling_llm',
            'timestamp': datetime.now().isoformat()
        })
        
        # LLM 클라이언트 가져오기 (폴백 전략 적용)
        llm_client = registry.get_client_with_fallback()
        
        # LangChain 메시지 변환
        from langchain_core.messages import SystemMessage, HumanMessage
        langchain_messages = []
        for msg in prompt_messages:
            if msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
        
        # 동기 LLM 호출 (책임 분리)
        response_content = llm_client.invoke(langchain_messages)
        logger.info(f"LLM response received for {resume_id}")
        
        # 4. 응답 파싱 (90%)
        set_task_progress(self.request.id, {
            'state': 'PROGRESS',
            'progress': 90,
            'message': '응답을 처리하고 결과를 저장하고 있습니다...',
            'stage': 'processing_response',
            'timestamp': datetime.now().isoformat()
        })
        
        # JSON 파싱 (문자열 응답 처리)
        parsed_response = parse_llm_json_response(
            response_content,
            expected_keys=["questions"],
            fallback_keys={"interview_questions": ["questions"]}
        )
        
        # 결과 구성
        result = {
            "resume_id": resume_id,
            "questions": parsed_response.get("questions", []),
            "generated_at": datetime.now().isoformat(),
            "model_used": llm_client.name,
            "task_id": self.request.id
        }
        
        # 5. DB 저장 및 완료 (100%)
        interview_collection = db.interview_questions
        insert_result = interview_collection.insert_one(result)
        
        # ObjectId를 문자열로 변환하여 serialization 문제 해결
        result["_id"] = str(insert_result.inserted_id)
        
        set_task_progress(self.request.id, {
            'state': 'SUCCESS',
            'progress': 100,
            'message': '면접 질문 생성이 완료되었습니다!',
            'stage': 'completed',
            'timestamp': datetime.now().isoformat(),
            'result': result
        })
        
        logger.info(f"Interview questions generated successfully for {resume_id}")
        return result
        
    except Exception as exc:
        error_message = f"면접 질문 생성 중 오류가 발생했습니다: {str(exc)}"
        logger.error(f"Error generating interview questions for {resume_id}: {exc}")
        
        set_task_progress(self.request.id, {
            'state': 'FAILURE',
            'progress': 0,
            'message': error_message,
            'stage': 'failed',
            'error': str(exc),
            'timestamp': datetime.now().isoformat()
        })
        # Use simple exception to avoid serialization issues
        raise RuntimeError(str(exc))

@current_app.task(name='tasks.get_task_progress')
def get_task_progress(task_id: str) -> Dict[str, Any]:
    """
    작업 진행 상황 조회 (Redis 직접 사용)
    """
    return get_task_progress_from_redis(task_id)
