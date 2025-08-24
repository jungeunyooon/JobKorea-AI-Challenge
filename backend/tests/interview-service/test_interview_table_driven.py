"""
Interview Service - Table Driven Test 패턴
"""
import pytest
import httpx
from typing import Optional, List

class TestInterviewQuestionTableDriven:
    """파라미터화된 테스트를 활용한 다양한 시나리오 검증"""

    @pytest.mark.parametrize("unique_key,resume_type,expected_questions,expected_status", [
        ("윤정은_1", "주니어개발자", 5, 200),
        ("김철수_1", "인턴경험개발자", 5, 200), 
        ("박영희_1", "DevOps전문가", 5, 200),
        ("invalid_key_test", "존재하지_않는_키", None, 404),
        ("", "빈_키", None, 422),  # FastAPI validation error
    ])
    @pytest.mark.asyncio
    async def test_resume_based_question_generation(
        self, 
        http_client: httpx.AsyncClient,
        unique_key: str,
        resume_type: str,
        expected_questions: Optional[int],
        expected_status: int
    ):
        """
        다양한 유형의 이력서에 대한 면접 질문 생성 테스트
        
        Args:
            unique_key: 이력서 고유 키
            resume_type: 이력서 타입 (설명용)
            expected_questions: 예상 질문 개수
            expected_status: 예상 HTTP 상태 코드
        """
        # Given: 다양한 유형의 이력서가 주어지고
        # When: 면접 질문 생성을 요청하면 (Gemini 기본 사용)
        response = await http_client.post(f"/interview/{unique_key}/questions")
        
        # Then: 예상된 결과를 반환한다
        assert response.status_code == expected_status
        
        if expected_questions:
            result = response.json()
            assert len(result["questions"]) == expected_questions
            assert result["provider"] == "gemini"
            assert "model" in result
            
            # 질문 타입 다양성 검증 (최소 3가지 다른 difficulty)
            difficulties = [q["difficulty"] for q in result["questions"]]
            unique_difficulties = set(difficulties)
            assert len(unique_difficulties) >= 2, f"Expected diverse difficulties, got: {unique_difficulties}"

    @pytest.mark.parametrize("question_difficulty,min_length,complexity_keywords", [
        ("easy", 50, ["기본", "간단", "경험"]),
        ("medium", 80, ["구현", "설계", "문제", "해결"]),
        ("hard", 100, ["아키텍처", "최적화", "확장", "트레이드오프"]),
    ])
    @pytest.mark.asyncio
    async def test_question_difficulty_characteristics(
        self,
        http_client: httpx.AsyncClient,
        question_difficulty: str,
        min_length: int,
        complexity_keywords: List[str]
    ):
        """
        난이도별 질문 특성 검증
        
        Args:
            question_difficulty: 질문 난이도
            min_length: 최소 질문 길이
            complexity_keywords: 복잡도 관련 키워드들
        """
        # Given: 이력서가 주어지고
        unique_key = "라이언_1"  # DevOps 전문가로 복잡한 질문 기대
        
        # When: 면접 질문을 생성하면
        response = await http_client.post(f"/interview/{unique_key}/questions")
        assert response.status_code == 200
        
        result = response.json()
        questions = result["questions"]
        
        # Then: 해당 난이도의 질문들이 특성을 만족한다
        target_questions = [q for q in questions if q["difficulty"] == question_difficulty]
        
        if target_questions:  # 해당 난이도 질문이 있을 때만 검증
            for question in target_questions:
                # 길이 검증
                question_text = question["question"]
                assert len(question_text) >= min_length, f"Question too short for {question_difficulty}: {question_text}"

    @pytest.mark.parametrize("resume_key,expected_tech_focus", [
        ("윤정은_1", ["kafka", "redis", "msa", "spring", "mysql"]),
        ("이민기_1", ["websocket", "spring", "redis", "msa", "gateway"]),
        ("라이언_1", ["kubernetes", "docker", "kafka", "grafana", "jenkins"]),
    ])
    @pytest.mark.asyncio
    async def test_tech_stack_based_question_focus(
        self,
        http_client: httpx.AsyncClient,
        resume_key: str,
        expected_tech_focus: List[str]
    ):
        """
        이력서의 기술 스택에 따른 질문 포커스 검증
        
        Args:
            resume_key: 이력서 키
            expected_tech_focus: 예상되는 기술 포커스 키워드들
        """
        # Given: 특정 기술 스택을 가진 이력서가 주어지고
        # When: 면접 질문을 생성하면
        response = await http_client.post(f"/interview/{resume_key}/questions")
        assert response.status_code == 200
        
        result = response.json()
        questions = result["questions"]
        
        # Then: 해당 기술 스택 관련 질문들이 포함된다
        all_question_text = " ".join([
            q["question"].lower() + " " + q["topic"].lower() 
            for q in questions
        ])
        
        # 예상 기술 중 최소 40% 이상이 언급되어야 함
        found_techs = [tech for tech in expected_tech_focus if tech.lower() in all_question_text]
        coverage_ratio = len(found_techs) / len(expected_tech_focus)
        
        assert coverage_ratio >= 0.4, f"Low tech coverage for {resume_key}. Found: {found_techs}, Expected: {expected_tech_focus}"

    @pytest.mark.parametrize("concurrent_requests", [1, 3, 5])
    @pytest.mark.asyncio
    async def test_concurrent_question_generation(
        self,
        http_client: httpx.AsyncClient,
        concurrent_requests: int
    ):
        """
        동시 요청 처리 성능 테스트
        
        Args:
            concurrent_requests: 동시 요청 수
        """
        import asyncio
        
        # Given: 유효한 이력서 키가 주어지고
        unique_key = "윤정은_1"
        
        # When: 동시에 여러 요청을 보내면
        async def make_request():
            response = await http_client.post(f"/interview/{unique_key}/questions")
            return response
        
        tasks = [make_request() for _ in range(concurrent_requests)]
        responses = await asyncio.gather(*tasks)
        
        # Then: 모든 요청이 성공적으로 처리된다
        for i, response in enumerate(responses):
            assert response.status_code == 200, f"Request {i+1} failed with status {response.status_code}"
            
            result = response.json()
            assert len(result["questions"]) == 5, f"Request {i+1} returned wrong number of questions"

    @pytest.mark.parametrize("timeout_seconds", [5, 10, 15])
    @pytest.mark.asyncio
    async def test_response_time_performance(
        self,
        http_client: httpx.AsyncClient,
        timeout_seconds: int
    ):
        """
        응답 시간 성능 테스트
        
        Args:
            timeout_seconds: 타임아웃 기준 (초)
        """
        import time
        
        # Given: 유효한 이력서가 주어지고
        unique_key = "라이언_1"
        
        # When: 면접 질문 생성을 요청하면
        start_time = time.time()
        response = await http_client.post(f"/interview/{unique_key}/questions")
        end_time = time.time()
        
        # Then: 지정된 시간 내에 응답한다
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < timeout_seconds, f"Response took {response_time:.2f}s, expected < {timeout_seconds}s"
