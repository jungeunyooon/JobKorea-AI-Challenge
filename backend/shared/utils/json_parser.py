"""
LLM 응답 JSON 파싱 공통 유틸리티
"""

import json
import re
from shared.utils.logger import setup_logger
from typing import Dict, Any, List, Union
try:
    from config import settings
    log_level = settings.log_level
except ImportError:
    log_level = "INFO"

logger = setup_logger("shared-json-parser", log_level)


def parse_llm_json_response(
    response_text: Union[str, Dict, List],
    expected_keys: List[str] = None,
    fallback_keys: Dict[str, List[str]] = None
) -> Dict[str, Any]:
    """
    LLM 응답에서 JSON을 파싱하는 견고한 함수
    
    Args:
        response_text: LLM의 원본 응답 (문자열 또는 이미 파싱된 객체)
        expected_keys: 기대하는 JSON 키 리스트 (예: ["questions", "learning_paths"])
        fallback_keys: 키별 대체 키 매핑 (예: {"questions": ["interview_questions", "result"]})
    
    Returns:
        파싱된 JSON 딕셔너리
        
    Raises:
        ValueError: JSON 파싱 실패 시
    """
    logger.info(f"About to parse JSON from LLM response. Type: {type(response_text)}")
    original_response = response_text
    
    try:
        # Step 0: 이미 파싱된 객체인지 확인
        if isinstance(response_text, (dict, list)):
            logger.info(f"Response is already parsed as {type(response_text)}")
            parsed_response = response_text
        else:
            # 문자열인 경우 기존 파싱 로직 수행
            logger.info(f"Response is string, parsing...")
            parsed_response = _parse_string_response(str(response_text))
        
        # Step 6: 키 매핑 및 정규화 (옵션)
        if expected_keys and fallback_keys:
            parsed_response = _normalize_response_keys(parsed_response, expected_keys, fallback_keys)
        
        # 디버깅용 로그
        if isinstance(parsed_response, dict):
            for key in parsed_response.keys():
                value = parsed_response[key]
                value_info = f"{len(value)} items" if isinstance(value, list) else str(type(value).__name__)
                logger.info(f"Response key found: '{key}' with {value_info}")
        
        return parsed_response
        
    except Exception as e:
        logger.error(f"Failed to parse LLM JSON response: {e}")
        logger.error(f"Original response type: {type(original_response)}, value: {str(original_response)[:500]}")
        raise ValueError(f"Failed to parse LLM JSON response: {e}")


def _parse_string_response(response_text: str) -> Union[Dict, List]:
    """문자열 응답을 파싱하는 함수"""
    try:
        # Step 1: 마크다운 블록 추출
        if "```json" in response_text:
            start_marker = "```json"
            start = response_text.find(start_marker)
            if start != -1:
                start += len(start_marker)
                # 개행문자 건너뛰기
                while start < len(response_text) and response_text[start] in ['\n', '\r', ' ']:
                    start += 1
                
                # 종료 ``` 찾기
                end = response_text.find("```", start)
                if end != -1:
                    response_text = response_text[start:end].strip()
                else:
                    response_text = response_text[start:].strip()
        
        # Step 2: 기본 정리
        response_text = response_text.strip()
        if response_text.startswith('```'):
            response_text = response_text[3:].strip()
        if response_text.endswith('```'):
            response_text = response_text[:-3].strip()
        
        # Step 3: 마크다운 및 특수문자 정리
        # 마크다운 볼드(**text**) 제거
        response_text = re.sub(r'\*\*(.*?)\*\*', r'\1', response_text)
        # 마크다운 이탤릭(*text*) 제거  
        response_text = re.sub(r'\*(.*?)\*', r'\1', response_text)
        # 백슬래시 이스케이프 처리
        response_text = response_text.replace('\\"', '"')
        
        logger.info(f"Cleaned JSON (first 200 chars): {response_text[:200]}")
        
        # Step 4: 빈 응답 체크
        if not response_text:
            raise ValueError("Empty JSON response after extraction")
        
        # Step 5: JSON 파싱 시도
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"Problematic JSON around error: {response_text[max(0, e.pos-50):e.pos+50]}")
            
            # 추가 정리 시도: 개행문자를 공백으로
            response_text_cleaned = response_text.replace('\n', ' ').replace('\r', ' ')
            # 연속 공백 제거
            response_text_cleaned = re.sub(r'\s+', ' ', response_text_cleaned)
            logger.info(f"Retry with cleaned newlines")
            
            try:
                return json.loads(response_text_cleaned)
            except json.JSONDecodeError as e2:
                logger.error(f"Failed to parse string response: {e2}")
                
                # 마지막 시도: 잘린 JSON 복구
                return _repair_truncated_json(response_text_cleaned)
        
    except Exception as e:
        logger.error(f"Failed to parse string response: {e}")
        raise


def _normalize_response_keys(
    parsed_response: Dict[str, Any],
    expected_keys: List[str],
    fallback_keys: Dict[str, List[str]]
) -> Dict[str, Any]:
    """응답의 키를 정규화 (다양한 키 패턴을 표준 키로 변환)"""
    normalized = {}
    
    for expected_key in expected_keys:
        # 1. 기본 키 확인
        if expected_key in parsed_response:
            normalized[expected_key] = parsed_response[expected_key]
            continue
            
        # 2. 대체 키 확인
        found = False
        if expected_key in fallback_keys:
            for fallback_key in fallback_keys[expected_key]:
                if fallback_key in parsed_response:
                    normalized[expected_key] = parsed_response[fallback_key]
                    found = True
                    logger.info(f"Used fallback key '{fallback_key}' for '{expected_key}'")
                    break
        
        # 3. 키를 찾지 못한 경우
        if not found:
            logger.warning(f"Expected key '{expected_key}' not found in response")
            normalized[expected_key] = []  # 기본값
    
    # 다른 키들도 복사
    for key, value in parsed_response.items():
        if key not in normalized:
            normalized[key] = value
    
    return normalized


def _repair_truncated_json(json_text: str) -> Dict[str, Any]:
    """잘린 JSON을 복구하는 함수"""
    logger.warning("Attempting to repair truncated JSON")
    
    try:
        # questions 배열이 있는지 확인
        if '"questions"' in json_text and '[' in json_text:
            # questions 배열의 시작 위치 찾기
            questions_start = json_text.find('"questions"')
            array_start = json_text.find('[', questions_start)
            
            if array_start != -1:
                # 배열의 끝을 찾기 위해 중괄호와 대괄호 카운트
                brace_count = 0
                bracket_count = 1  # 이미 [를 찾았으므로 1부터 시작
                end_pos = array_start + 1
                
                for i, char in enumerate(json_text[array_start + 1:], array_start + 1):
                    if char == '[':
                        bracket_count += 1
                    elif char == ']':
                        bracket_count -= 1
                    elif char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    
                    if bracket_count == 0 and brace_count == 0:
                        end_pos = i + 1
                        break
                
                # 복구된 JSON 생성
                repaired_json = json_text[:end_pos] + ']}'
                logger.info(f"Repaired JSON (first 200 chars): {repaired_json[:200]}")
                
                return json.loads(repaired_json)
        
        # 기본 복구: 마지막 완전한 객체까지만 사용
        if '"questions"' in json_text:
            # 마지막 완전한 질문 객체 찾기
            last_complete_question = _find_last_complete_question(json_text)
            if last_complete_question:
                repaired_json = '{"questions": [' + last_complete_question + ']}'
                logger.info(f"Using last complete question: {repaired_json[:200]}")
                return json.loads(repaired_json)
        
        # 최후의 수단: 빈 questions 배열 반환
        logger.warning("Could not repair JSON, returning empty questions array")
        return {"questions": []}
        
    except Exception as e:
        logger.error(f"Failed to repair JSON: {e}")
        return {"questions": []}


def _find_last_complete_question(json_text: str) -> str:
    """마지막 완전한 질문 객체를 찾는 함수"""
    try:
        # questions 배열 내의 각 질문 객체 찾기
        questions_start = json_text.find('"questions"')
        array_start = json_text.find('[', questions_start)
        
        if array_start == -1:
            return None
        
        # 각 질문 객체의 시작과 끝 찾기
        brace_count = 0
        question_start = None
        questions = []
        
        for i, char in enumerate(json_text[array_start + 1:], array_start + 1):
            if char == '{':
                if brace_count == 0:
                    question_start = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and question_start is not None:
                    question = json_text[question_start:i + 1]
                    # 간단한 유효성 검사
                    if '"question"' in question and '"difficulty"' in question:
                        questions.append(question)
                    question_start = None
        
        # 마지막 완전한 질문 반환
        if questions:
            return questions[-1]
        
        return None
        
    except Exception as e:
        logger.error(f"Error finding last complete question: {e}")
        return None
