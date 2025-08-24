"""
면접 질문 생성 서비스 함수들
"""
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from shared.llm.registry import registry
from shared.prompts.loader import get_prompt_loader
from shared.utils.resume_formatter import format_resume_for_interview
from shared.utils.json_parser import parse_llm_json_response
from .crud import get_resume_by_unique_key, create_interview_questions

logger = logging.getLogger(__name__)

def _create_interview_prompt(formatted_data: Dict[str, Any]) -> List:
    """면접 질문 생성 프롬프트 생성 (YAML 파일 기반)"""
    try:
        # 프롬프트 로더 가져오기
        loader = get_prompt_loader('interview')
        
        # 프롬프트 설정 로드
        config = loader.load_prompt_config('interview_questions.yaml')
        
        # 경력 레벨 결정
        years_exp = formatted_data.get('years_experience', 0)
        experience_level = loader.get_experience_level(years_exp)
        
        logger.info(f"경력 {years_exp}년 → {experience_level} 레벨로 분류")
        
        # 시스템 프롬프트 렌더링
        system_prompt = loader.render_system_prompt(config, {
            'experience_level': experience_level
        })
        
        # 휴먼 프롬프트 렌더링
        human_prompt = loader.render_human_prompt(config, formatted_data)
        
        return [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
    except Exception as e:
        logger.error(f"프롬프트 생성 실패: {e}")
        # 폴백: 간단한 기본 프롬프트
        return _create_fallback_prompt(formatted_data)

def _create_fallback_prompt(formatted_data: Dict[str, Any]) -> List:
    """YAML 로드 실패 시 사용할 폴백 프롬프트"""
    system_prompt = """
당신은 백엔드 개발자 채용 전문 기술 면접관입니다.
주어진 이력서 정보를 바탕으로 개인 맞춤형 면접 질문 5개를 생성해주세요.

중요: 
- 마크다운 문법(**굵은글씨**, *기울임*) 사용 금지
- 순수 텍스트만 사용하세요
- JSON 형식을 정확히 지켜주세요

응답은 다음 JSON 형식으로만 제공해주세요:
{
  "questions": [
    {
      "difficulty": "easy|medium|hard",
      "topic": "주요 기술 키워드",
      "question": "실제 질문 본문",
      "what_good_answers_cover": ["좋은 답변이 포함해야 할 핵심 요소"]
    }
  ]
}
"""
        
    human_prompt = f"""
    지원자 정보:
    이름: {formatted_data['name']}
    경력: {formatted_data['experience_months']}개월

    프로젝트 경험:
    {formatted_data['projects']}

    위 프로젝트 경험을 바탕으로 개인 맞춤형 면접 질문 5개를 생성해주세요.
    각 질문은 구체적인 프로젝트나 기술 경험을 언급해야 합니다.
    """
    
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

async def generate_interview_questions_service(unique_key: str, provider: str = "gemini") -> Dict[str, Any]:
    """면접 질문 생성 서비스 함수"""
    try:
        logger.error(f"Starting interview questions generation for {unique_key}")
        
        # 이력서 조회
        try:
            resume_data = await get_resume_by_unique_key(unique_key)
            logger.error(f"Resume data retrieved successfully")
            logger.error(f"Resume data type: {type(resume_data)}")
            
            if not resume_data:
                raise Exception("Resume not found")
                
        except Exception as e:
            logger.error(f"Error in get_resume_by_unique_key: {e}")
            raise e
        
        # 이력서 데이터 포맷팅 (면접 질문용)
        try:
            formatted_data = format_resume_for_interview(resume_data)
            logger.error(f"Resume data formatted successfully: {formatted_data}")
        except Exception as e:
            logger.error(f"Error in format_resume_for_interview: {e}")
            logger.error(f"Resume data causing error: {resume_data}")
            raise e
        
        # 지정된 LLM 클라이언트 가져오기
        llm_client = registry.get_client(provider)
        logger.error(f"Requested provider: {provider}")
        logger.error(f"LLM client: {llm_client}")
        logger.error(f"Available clients: {registry.get_available_clients()}")
        
        if not llm_client:
            # 폴백 시도
            llm_client = registry.get_client_with_fallback()
            if llm_client:
                logger.warning(f"Provider '{provider}' not available, using fallback: {llm_client.name}")
            else:
                raise Exception(f"LLM provider '{provider}' not available and no fallback available")
        
        # 프롬프트 생성
        try:
            logger.error(f"About to create interview prompt with formatted_data: {formatted_data}")
            messages = _create_interview_prompt(formatted_data)
            logger.error(f"Interview prompt created successfully")
        except Exception as e:
            logger.error(f"Error in _create_interview_prompt: {e}")
            logger.error(f"Formatted data causing error: {formatted_data}")
            raise e
        
        # LLM 호출
        try:
            logger.error(f"About to call LLM with messages count: {len(messages)}")
            response_text = await llm_client.ainvoke(messages)
            logger.error(f"LLM response received: {type(response_text)}, length: {len(response_text) if response_text else 0}")
            logger.error(f"LLM response content (first 200 chars): {response_text[:200] if response_text else 'None'}")
        except Exception as e:
            logger.error(f"Error in LLM call: {e}")
            raise e
        
        # JSON 파싱 - 공통 유틸리티 사용
        try:
            parsed_response = parse_llm_json_response(
                response_text,
                expected_keys=["questions"],
                fallback_keys={"questions": ["interview_questions", "result"]}
            )
            
            # 질문 추출 (다양한 응답 형태 처리)
            if isinstance(parsed_response, list):
                # LLM이 직접 질문 배열로 응답한 경우: [{...}, {...}, ...]
                questions = parsed_response
                logger.error(f"Questions found as direct array: count: {len(questions)}")
            elif isinstance(parsed_response, dict):
                # LLM이 올바른 스키마로 응답한 경우: {"questions": [...]}
                # 공통 파싱에서 이미 키 매핑 처리됨
                questions = parsed_response.get("questions", [])
                logger.error(f"Questions extracted from dict: count: {len(questions)}")
            else:
                logger.error(f"Unexpected response type: {type(parsed_response)}")
                questions = []
            
            if not isinstance(questions, list) or len(questions) == 0:
                raise ValueError("No valid questions in response")
            
            # 데이터베이스에 저장 (Provider 및 Model 정보 포함)
            interview_data = {
                "unique_key": unique_key,
                "provider": provider,
                "model": llm_client._model,  # 실제 사용된 모델명 저장
                "questions": questions[:5],  # 최대 5개
                "created_at": datetime.utcnow(),
                "resume_id": resume_data["id"],
                "session_id": f"{unique_key}_{provider}_{int(datetime.utcnow().timestamp())}"
            }
            
            interview_id = await create_interview_questions(interview_data)
            
            return {
                "interview_id": interview_id,
                "resume_id": resume_data["id"],
                "unique_key": unique_key,
                "provider": provider,
                "model": llm_client._model,
                "questions": questions[:5],
                "generated_at": datetime.utcnow()
            }
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise Exception("Failed to generate interview questions")
        
    except Exception as e:
        logger.error(f"Error generating interview questions: {e}")
        raise e