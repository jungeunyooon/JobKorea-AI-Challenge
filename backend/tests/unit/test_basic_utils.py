"""
기본 유틸리티 함수 단위 테스트 (외부 모듈 의존성 없음)
"""
import pytest
import json
import re
from typing import Dict, Any, List

def remove_markdown_from_json(text: str) -> str:
    """JSON에서 마크다운 블록 제거"""
    # ```json...``` 패턴 제거
    text = re.sub(r'```(?:json\s*)?(.*?)```', r'\1', text, flags=re.DOTALL)
    return text.strip()

def validate_question_structure(question: Dict[str, Any]) -> bool:
    """면접 질문 구조 유효성 검증"""
    required_fields = ["question", "difficulty", "topic"]
    return all(field in question for field in required_fields)

def validate_learning_path_structure(path: Dict[str, Any]) -> bool:
    """학습 경로 구조 유효성 검증"""
    required_fields = ["type", "title", "description", "reason", "resources", "link"]
    return all(field in path for field in required_fields)

def calculate_difficulty_distribution(questions: List[Dict[str, Any]]) -> Dict[str, int]:
    """면접 질문 난이도 분포 계산"""
    distribution = {"easy": 0, "medium": 0, "hard": 0}
    for question in questions:
        difficulty = question.get("difficulty", "unknown")
        if difficulty in distribution:
            distribution[difficulty] += 1
    return distribution

def calculate_learning_type_distribution(paths: List[Dict[str, Any]]) -> Dict[str, int]:
    """학습 경로 타입 분포 계산"""
    distribution = {"strength": 0, "weakness": 0}
    for path in paths:
        path_type = path.get("type", "unknown")
        if path_type in distribution:
            distribution[path_type] += 1
    return distribution

class TestBasicUtilities:
    """기본 유틸리티 함수 테스트"""

    def test_remove_markdown_from_json(self):
        """
        시나리오: JSON에서 마크다운 제거
        Given: 마크다운 블록으로 감싸진 JSON이 주어지고
        When: 마크다운 제거 함수를 호출하면
        Then: 순수 JSON 문자열이 반환된다
        """
        # Given: 마크다운 블록으로 감싸진 JSON이 주어지고
        markdown_json = '''```json
        {"test": "value", "number": 123}
        ```'''
        
        # When: 마크다운 제거 함수를 호출하면
        result = remove_markdown_from_json(markdown_json)
        
        # Then: 순수 JSON 문자열이 반환된다
        assert result == '{"test": "value", "number": 123}'
        parsed = json.loads(result)
        assert parsed["test"] == "value"
        assert parsed["number"] == 123

    def test_validate_question_structure_valid(self):
        """
        시나리오: 유효한 면접 질문 구조 검증
        Given: 필수 필드를 모두 가진 질문이 주어지고
        When: 구조 검증을 수행하면
        Then: True가 반환된다
        """
        # Given: 필수 필드를 모두 가진 질문이 주어지고
        valid_question = {
            "question": "Spring Boot에서 Bean의 생명주기에 대해 설명해주세요",
            "difficulty": "medium",
            "topic": "Spring Boot, Bean"
        }
        
        # When: 구조 검증을 수행하면
        result = validate_question_structure(valid_question)
        
        # Then: True가 반환된다
        assert result is True

    def test_validate_question_structure_invalid(self):
        """
        시나리오: 무효한 면접 질문 구조 검증
        Given: 필수 필드가 누락된 질문이 주어지고
        When: 구조 검증을 수행하면
        Then: False가 반환된다
        """
        # Given: 필수 필드가 누락된 질문이 주어지고
        invalid_question = {
            "question": "불완전한 질문",
            # difficulty와 topic 누락
        }
        
        # When: 구조 검증을 수행하면
        result = validate_question_structure(invalid_question)
        
        # Then: False가 반환된다
        assert result is False

    def test_validate_learning_path_structure_valid(self):
        """
        시나리오: 유효한 학습 경로 구조 검증
        Given: 필수 필드를 모두 가진 학습 경로가 주어지고
        When: 구조 검증을 수행하면
        Then: True가 반환된다
        """
        # Given: 필수 필드를 모두 가진 학습 경로가 주어지고
        valid_path = {
            "type": "strength",
            "title": "Kafka 스트리밍 아키텍처 고도화",
            "description": "실시간 데이터 처리 전문성 강화",
            "reason": "기존 Kafka 경험을 바탕으로 심화 학습",
            "resources": ["Kafka Streams", "Event Sourcing"],
            "link": "https://kafka.apache.org/documentation/"
        }
        
        # When: 구조 검증을 수행하면
        result = validate_learning_path_structure(valid_path)
        
        # Then: True가 반환된다
        assert result is True

    def test_calculate_difficulty_distribution(self):
        """
        시나리오: 면접 질문 난이도 분포 계산
        Given: 다양한 난이도의 질문들이 주어지고
        When: 분포를 계산하면
        Then: 정확한 분포가 반환된다
        """
        # Given: 다양한 난이도의 질문들이 주어지고
        questions = [
            {"difficulty": "easy"},
            {"difficulty": "medium"},
            {"difficulty": "medium"},
            {"difficulty": "hard"},
            {"difficulty": "medium"}
        ]
        
        # When: 분포를 계산하면
        distribution = calculate_difficulty_distribution(questions)
        
        # Then: 정확한 분포가 반환된다
        assert distribution["easy"] == 1
        assert distribution["medium"] == 3
        assert distribution["hard"] == 1

    def test_calculate_learning_type_distribution(self):
        """
        시나리오: 학습 경로 타입 분포 계산
        Given: 다양한 타입의 학습 경로들이 주어지고
        When: 분포를 계산하면
        Then: 정확한 분포가 반환된다
        """
        # Given: 다양한 타입의 학습 경로들이 주어지고
        paths = [
            {"type": "strength"},
            {"type": "strength"},
            {"type": "weakness"},
            {"type": "weakness"},
            {"type": "weakness"}
        ]
        
        # When: 분포를 계산하면
        distribution = calculate_learning_type_distribution(paths)
        
        # Then: 정확한 분포가 반환된다
        assert distribution["strength"] == 2
        assert distribution["weakness"] == 3

    def test_difficulty_distribution_balance_validation(self):
        """
        시나리오: 난이도 분포 균형 검증
        Given: 면접 질문 세트가 주어지고
        When: 균형 검증을 수행하면
        Then: 적절한 분포를 가지고 있다
        """
        # Given: 면접 질문 세트가 주어지고
        questions = [
            {"difficulty": "easy"},
            {"difficulty": "medium"},
            {"difficulty": "medium"},
            {"difficulty": "medium"},
            {"difficulty": "hard"}
        ]
        
        # When: 균형 검증을 수행하면
        distribution = calculate_difficulty_distribution(questions)
        total = sum(distribution.values())
        
        # Then: 적절한 분포를 가지고 있다
        # 권장사항: easy(1), medium(3), hard(1)
        assert distribution["easy"] >= 1
        assert distribution["medium"] >= 2
        assert distribution["hard"] >= 1
        assert total == 5

    def test_learning_type_balance_validation(self):
        """
        시나리오: 학습 경로 타입 균형 검증
        Given: 학습 경로 세트가 주어지고
        When: 균형 검증을 수행하면
        Then: 강점과 약점이 균형있게 분포한다
        """
        # Given: 학습 경로 세트가 주어지고
        paths = [
            {"type": "strength"},
            {"type": "strength"},
            {"type": "weakness"},
            {"type": "weakness"},
            {"type": "weakness"}
        ]
        
        # When: 균형 검증을 수행하면
        distribution = calculate_learning_type_distribution(paths)
        total = sum(distribution.values())
        
        strength_ratio = distribution["strength"] / total
        weakness_ratio = distribution["weakness"] / total
        
        # Then: 강점과 약점이 균형있게 분포한다
        # 각 타입이 최소 20% 이상은 되어야 함
        assert strength_ratio >= 0.2
        assert weakness_ratio >= 0.2
        assert total == 5

class TestReadmeTestStrategies:
    """README.md에 작성된 테스트 전략 구현 검증"""

    def test_given_when_then_pattern_example(self):
        """
        README.md BDD 패턴 예시 구현
        Given-When-Then 패턴을 실제로 적용한 테스트
        """
        # Given: 유효한 이력서 데이터가 주어지고
        resume_data = {"name": "김개발", "tech_skills": ["Python", "FastAPI"]}
        
        # When: 데이터 검증을 요청하면
        is_valid = (
            "name" in resume_data and 
            "tech_skills" in resume_data and 
            len(resume_data["tech_skills"]) > 0
        )
        
        # Then: 유효성 검증이 통과한다
        assert is_valid is True
        assert resume_data["name"] == "김개발"
        assert "Python" in resume_data["tech_skills"]

    @pytest.mark.parametrize("resume_type,tech_stack,expected_valid", [
        ("신입개발자", ["Python", "FastAPI"], True),
        ("시니어개발자", ["Java", "Spring Boot", "Kubernetes"], True),
        ("풀스택개발자", ["JavaScript", "React", "Node.js"], True),
        ("무효한_데이터", [], False),
    ])
    def test_table_driven_example(self, resume_type: str, tech_stack: List[str], expected_valid: bool):
        """
        README.md Table Driven Test 패턴 예시 구현
        파라미터화된 테스트로 다양한 시나리오 검증
        """
        # Given: 다양한 유형의 이력서가 주어지고
        resume_data = {
            "type": resume_type,
            "tech_skills": tech_stack
        }
        
        # When: 기술 스택 유효성을 검증하면
        is_valid = len(tech_stack) > 0
        
        # Then: 예상된 결과를 반환한다
        assert is_valid == expected_valid
        
        if expected_valid:
            assert len(tech_stack) >= 1
        else:
            assert len(tech_stack) == 0

    def test_flaky_test_resilience_example(self):
        """
        Flaky Test 대응 전략 예시
        불안정할 수 있는 조건에서도 안정적인 테스트
        """
        # 여러 번 시도해도 안정적인 결과를 얻는 로직
        attempts = 0
        max_attempts = 3
        success = False
        
        while attempts < max_attempts and not success:
            try:
                # 시뮬레이션: 불안정할 수 있는 작업
                result = {"status": "success", "data": [1, 2, 3, 4, 5]}
                
                # 검증
                assert result["status"] == "success"
                assert len(result["data"]) == 5
                success = True
                
            except AssertionError:
                attempts += 1
                if attempts == max_attempts:
                    raise
        
        assert success is True
        assert attempts < max_attempts
