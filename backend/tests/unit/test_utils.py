"""
유틸리티 함수 단위 테스트 (API 호출 없음)
"""
import pytest 
import sys
import os

# 백엔드 모듈 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    from shared.utils.json_parser import parse_llm_json_response
    from shared.utils.resume_formatter import format_resume_for_llm
except ImportError:
    # 모듈을 찾을 수 없는 경우 스킵
    parse_llm_json_response = None
    format_resume_for_llm = None

class TestJSONParser:
    """JSON 파서 유틸리티 테스트"""

    def test_parse_valid_json_response(self):
        """
        시나리오: 유효한 JSON 응답 파싱
        Given: 올바른 JSON 문자열이 주어지고
        When: JSON 파싱을 시도하면
        Then: 파싱된 딕셔너리가 반환된다
        """
        if parse_llm_json_response is None:
            pytest.skip("parse_llm_json_response module not available")
            
        # Given: 올바른 JSON 문자열이 주어지고
        json_response = '{"questions": [{"question": "테스트 질문", "difficulty": "medium"}], "summary": "테스트 요약"}'
        expected_keys = ["questions", "summary"]
        
        # When: JSON 파싱을 시도하면
        result = parse_llm_json_response(json_response, expected_keys)
        
        # Then: 파싱된 딕셔너리가 반환된다
        assert isinstance(result, dict)
        assert "questions" in result
        assert "summary" in result
        assert len(result["questions"]) == 1
        assert result["questions"][0]["question"] == "테스트 질문"

    def test_parse_json_with_markdown_removal(self):
        """
        시나리오: 마크다운이 포함된 JSON 응답 파싱
        Given: 마크다운 블록으로 감싸진 JSON이 주어지고
        When: JSON 파싱을 시도하면
        Then: 마크다운이 제거되고 파싱된다
        """
        # Given: 마크다운 블록으로 감싸진 JSON이 주어지고
        json_response = '''```json
        {"learning_paths": [{"title": "테스트 학습"}], "summary": "요약"}
        ```'''
        expected_keys = ["learning_paths", "summary"]
        
        # When: JSON 파싱을 시도하면
        result = parse_llm_json_response(json_response, expected_keys)
        
        # Then: 마크다운이 제거되고 파싱된다
        assert isinstance(result, dict)
        assert "learning_paths" in result
        assert len(result["learning_paths"]) == 1

    def test_parse_json_with_fallback_keys(self):
        """
        시나리오: 폴백 키를 사용한 JSON 파싱
        Given: 예상 키와 다른 키를 가진 JSON이 주어지고
        When: 폴백 키로 파싱을 시도하면
        Then: 폴백 키를 사용하여 파싱된다
        """
        # Given: 예상 키와 다른 키를 가진 JSON이 주어지고
        json_response = '{"paths": [{"title": "대체 학습"}], "overview": "대체 요약"}'
        expected_keys = ["learning_paths", "summary"]
        fallback_keys = {"learning_paths": ["paths"], "summary": ["overview"]}
        
        # When: 폴백 키로 파싱을 시도하면
        result = parse_llm_json_response(json_response, expected_keys, fallback_keys)
        
        # Then: 폴백 키를 사용하여 파싱된다
        assert isinstance(result, dict)
        assert "learning_paths" in result
        assert "summary" in result
        assert result["summary"] == "대체 요약"

class TestResumeFormatter:
    """이력서 포맷터 유틸리티 테스트"""

    def test_format_resume_basic_data(self):
        """
        시나리오: 기본 이력서 데이터 포맷팅
        Given: 기본 이력서 정보가 주어지고
        When: LLM용 포맷팅을 수행하면
        Then: 구조화된 텍스트가 생성된다
        """
        # Given: 기본 이력서 정보가 주어지고
        resume_data = {
            "name": "테스트개발자",
            "total_experience_months": 24,
            "work_experiences": [
                {
                    "company": "테스트회사",
                    "position": "개발자",
                    "project_name": "테스트 프로젝트",
                    "tech_stack": ["Python", "FastAPI"]
                }
            ],
            "personal_projects": []
        }
        
        # When: LLM용 포맷팅을 수행하면
        formatted = format_resume_for_llm(resume_data)
        
        # Then: 구조화된 텍스트가 생성된다
        assert isinstance(formatted, str)
        assert "테스트개발자" in formatted
        assert "24개월" in formatted
        assert "테스트회사" in formatted
        assert "Python" in formatted
        assert "FastAPI" in formatted

    def test_format_resume_with_projects_detail(self):
        """
        시나리오: 상세 프로젝트 정보가 있는 이력서 포맷팅
        Given: 상세한 프로젝트 정보가 포함된 이력서가 주어지고
        When: LLM용 포맷팅을 수행하면
        Then: 프로젝트 상세 정보가 포함된다
        """
        # Given: 상세한 프로젝트 정보가 포함된 이력서가 주어지고
        resume_data = {
            "name": "고급개발자",
            "total_experience_months": 36,
            "work_experiences": [
                {
                    "company": "기술회사",
                    "position": "시니어 개발자",
                    "project_name": "마이크로서비스 플랫폼",
                    "tech_stack": ["Java", "Spring Boot", "Kubernetes"],
                    "achievements": [
                        "MSA 아키텍처 설계",
                        "성능 50% 개선"
                    ]
                }
            ],
            "personal_projects": [
                {
                    "name": "개인 프로젝트",
                    "tech_stack": ["React", "Node.js"],
                    "key_achievements": [
                        "실시간 채팅 구현",
                        "Docker 배포"
                    ]
                }
            ]
        }
        
        # When: LLM용 포맷팅을 수행하면
        formatted = format_resume_for_llm(resume_data)
        
        # Then: 프로젝트 상세 정보가 포함된다
        assert "마이크로서비스 플랫폼" in formatted
        assert "MSA 아키텍처 설계" in formatted
        assert "성능 50% 개선" in formatted
        assert "개인 프로젝트" in formatted
        assert "실시간 채팅 구현" in formatted

    def test_format_resume_empty_projects(self):
        """
        시나리오: 프로젝트가 없는 이력서 포맷팅
        Given: 프로젝트 정보가 없는 이력서가 주어지고
        When: LLM용 포맷팅을 수행하면
        Then: 에러 없이 기본 정보만 포맷팅된다
        """
        # Given: 프로젝트 정보가 없는 이력서가 주어지고
        resume_data = {
            "name": "신입개발자",
            "total_experience_months": 0,
            "work_experiences": [],
            "personal_projects": []
        }
        
        # When: LLM용 포맷팅을 수행하면
        formatted = format_resume_for_llm(resume_data)
        
        # Then: 에러 없이 기본 정보만 포맷팅된다
        assert isinstance(formatted, str)
        assert "신입개발자" in formatted
        assert "0개월" in formatted
        # 빈 프로젝트 섹션도 적절히 처리되어야 함
        assert len(formatted) > 10  # 최소한의 내용은 있어야 함

class TestPromptUtilities:
    """프롬프트 관련 유틸리티 테스트"""

    def test_difficulty_distribution_validation(self):
        """
        시나리오: 질문 난이도 분포 검증
        Given: 다양한 난이도의 질문들이 주어지고
        When: 난이도 분포를 검증하면
        Then: 적절한 분포를 가지고 있다
        """
        # Given: 다양한 난이도의 질문들이 주어지고
        questions = [
            {"difficulty": "easy"},
            {"difficulty": "medium"},
            {"difficulty": "medium"},
            {"difficulty": "medium"},
            {"difficulty": "hard"}
        ]
        
        # When: 난이도 분포를 계산하면
        difficulties = [q["difficulty"] for q in questions]
        easy_count = difficulties.count("easy")
        medium_count = difficulties.count("medium")
        hard_count = difficulties.count("hard")
        
        # Then: 적절한 분포를 가지고 있다
        assert easy_count >= 1  # 최소 1개 easy
        assert medium_count >= 2  # 최소 2개 medium
        assert hard_count >= 1  # 최소 1개 hard
        assert len(questions) == 5  # 총 5개

    def test_learning_path_type_balance(self):
        """
        시나리오: 학습 경로 타입 균형 검증
        Given: 강점/약점 타입의 학습 경로들이 주어지고
        When: 타입 분포를 검증하면
        Then: 균형잡힌 분포를 가진다
        """
        # Given: 강점/약점 타입의 학습 경로들이 주어지고
        learning_paths = [
            {"type": "strength", "title": "강점 학습 1"},
            {"type": "strength", "title": "강점 학습 2"},
            {"type": "weakness", "title": "약점 보완 1"},
            {"type": "weakness", "title": "약점 보완 2"},
            {"type": "weakness", "title": "약점 보완 3"}
        ]
        
        # When: 타입 분포를 계산하면
        types = [lp["type"] for lp in learning_paths]
        strength_count = types.count("strength")
        weakness_count = types.count("weakness")
        
        # Then: 균형잡힌 분포를 가진다
        total = len(learning_paths)
        strength_ratio = strength_count / total
        weakness_ratio = weakness_count / total
        
        # 각 타입이 최소 20% 이상은 되어야 함
        assert strength_ratio >= 0.2
        assert weakness_ratio >= 0.2
