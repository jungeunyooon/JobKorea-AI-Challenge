"""
Learning Service 함수들
"""
import json
from shared.utils.logger import setup_logger
from typing import Dict, List, Any
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from shared.llm.registry import registry
from shared.prompts.loader import get_prompt_loader
from shared.utils.resume_formatter import format_resume_for_learning
from shared.utils.json_parser import parse_llm_json_response
from database import get_resumes_collection, get_learning_collection
from config import settings
    
logger = setup_logger("learning-service", settings.log_level)

def _create_learning_path_prompt(formatted_data: Dict[str, Any]) -> List:
    """학습 경로 추천 프롬프트 생성 (YAML 파일 기반)"""
    try:
        loader = get_prompt_loader('learning')
        config = loader.load_prompt_config('learning_path.yaml')
        
        # 시스템 프롬프트 렌더링
        system_prompt = loader.render_system_prompt(config)
        
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
당신은 경험이 풍부한 커리어 코치이자 기술 멘토입니다.
주어진 프로젝트 경험을 바탕으로 구직자의 역량을 강화하고 합격률을 높일 수 있는 개인 맞춤형 학습 경로를 제안해주세요.

중요: 
- 마크다운 문법 사용 금지
- 순수 텍스트만 사용하세요
- JSON 형식을 정확히 지켜주세요

응답은 다음 JSON 형식으로만 제공해주세요:
{
  "summary": "전체 학습 경로 요약 (3-4줄)",
  "learning_paths": [
    {
      "category": "기술스택|프로젝트|소프트스킬|자격증|포트폴리오",
      "title": "학습 제목",
      "description": "구체적인 학습 목표와 방법",
      "priority": 1-5,
      "estimated_weeks": 1-12,
      "resources": ["추천 학습 리소스1", "추천 학습 리소스2"]
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

위 프로젝트 경험을 분석하여 개인 맞춤형 학습 경로 6-8개를 생성해주세요.
현재 경험을 바탕으로 부족한 부분을 보완하고 강점을 더욱 발전시킬 수 있는 실무 중심의 학습 계획을 제안해주세요.
"""
    
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

async def generate_learning_path_service(unique_key: str, provider: str = "gemini") -> Dict[str, Any]:
    """학습 경로 생성 서비스 함수"""
    try:
        logger.info(f"Starting learning path generation for {unique_key}")
        
        # 이력서 조회
        resumes_collection = get_resumes_collection()
        resume = await resumes_collection.find_one({"unique_key": unique_key})
        
        if not resume:
            raise Exception("Resume not found")
        
        # 지정된 LLM 클라이언트 가져오기
        llm_client = registry.get_client(provider)
        logger.info(f"Requested provider: {provider}")
        logger.info(f"LLM client: {llm_client}")
        logger.info(f"Available clients: {registry.get_available_clients()}")
        
        if not llm_client:
            # 폴백 시도
            llm_client = registry.get_client_with_fallback()
            if llm_client:
                logger.warning(f"Provider '{provider}' not available, using fallback: {llm_client.name}")
            else:
                raise Exception(f"LLM provider '{provider}' not available and no fallback available")
        
        # 이력서 데이터 포맷팅 (학습 경로용)
        formatted_data = format_resume_for_learning(resume)
        
        # 프롬프트 생성
        messages = _create_learning_path_prompt(formatted_data)
        
        # LLM 호출
        response_text = await llm_client.ainvoke(messages)
        
        # JSON 파싱 - 공통 유틸리티 사용
        try:
            parsed_response = parse_llm_json_response(
                response_text,
                expected_keys=["analysis", "summary", "learning_paths"],
                fallback_keys={"learning_paths": ["paths", "recommendations"]}
            )
            
            analysis = parsed_response.get("analysis", {"strengths": [], "weaknesses": []})
            summary = parsed_response.get("summary", "")
            learning_paths = parsed_response.get("learning_paths", [])
            
            if not isinstance(learning_paths, list) or len(learning_paths) == 0:
                raise ValueError("No valid learning paths in response")
            
            # 데이터베이스에 저장 (Provider 및 Model 정보 포함)
            learning_data = {
                "unique_key": unique_key,
                "provider": provider,
                "model": llm_client._model,  # 실제 사용된 모델명 저장
                "analysis": analysis,
                "summary": summary,
                "learning_paths": learning_paths[:8],  # 최대 8개
                "created_at": datetime.utcnow(),
                "resume_id": str(resume["_id"]),
                "session_id": f"{unique_key}_{provider}_{int(datetime.utcnow().timestamp())}"
            }
            
            learning_collection = get_learning_collection()
            result = await learning_collection.insert_one(learning_data)
            
            return {
                "learning_id": str(result.inserted_id),
                "resume_id": str(resume["_id"]),
                "unique_key": unique_key,
                "provider": provider,
                "model": llm_client._model,  # 사용된 모델 정보 반환
                "analysis": analysis,
                "summary": summary,
                "learning_paths": learning_paths[:8],  # 최대 8개
                "generated_at": datetime.utcnow()
            }
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise Exception("Failed to generate learning path")
        
    except Exception as e:
        logger.error(f"Error generating learning path for {unique_key}: {e}")
        raise e
