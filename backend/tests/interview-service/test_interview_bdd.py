"""
Interview Service - Given-When-Then 패턴 테스트
"""
import pytest
import httpx
from typing import Dict, Any

class TestInterviewQuestionGenerationBDD:
    """Given-When-Then 패턴을 활용한 면접 질문 생성 테스트"""

    @pytest.mark.asyncio
    async def test_generate_interview_questions_for_existing_resume(
        self, 
        http_client: httpx.AsyncClient,
        existing_resume_keys: list
    ):
        """
        시나리오: 기존 이력서로 면접 질문 생성
        Given: 유효한 이력서 데이터가 주어지고
        When: 면접 질문 생성을 요청하면 (Gemini 기본 사용)
        Then: 5개의 면접 질문이 생성된다
        """
        # Given: 유효한 이력서 키가 주어지고
        unique_key = existing_resume_keys[0]  # 윤정은_1
        
        # When: 면접 질문 생성을 요청하면
        response = await http_client.post(f"/interview/{unique_key}/questions")
        
        # Then: 성공적으로 5개의 면접 질문이 생성된다
        assert response.status_code == 200
        
        result = response.json()
        assert "questions" in result
        assert len(result["questions"]) == 5
        assert all("question" in q for q in result["questions"])
        assert all("difficulty" in q for q in result["questions"])
        assert all("topic" in q for q in result["questions"])
        
        # 기본 모델 확인
        assert result["provider"] == "gemini"
        assert "model" in result
        assert "generated_at" in result

    @pytest.mark.asyncio
    async def test_generate_interview_questions_with_devops_expertise(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: DevOps 전문성을 가진 이력서로 면접 질문 생성
        Given: 라이언님의 Kubernetes/DevOps 전문 이력서가 주어지고
        When: 면접 질문 생성을 요청하면
        Then: DevOps 관련 전문적인 질문들이 생성된다
        """
        # Given: DevOps 전문가 이력서가 주어지고
        unique_key = "라이언_1"
        
        # When: 면접 질문 생성을 요청하면
        response = await http_client.post(f"/interview/{unique_key}/questions")
        
        # Then: DevOps 관련 전문 질문들이 생성된다
        assert response.status_code == 200
        
        result = response.json()
        questions = result["questions"]
        
        # DevOps 관련 키워드가 포함된 질문이 있는지 확인
        devops_keywords = ["kubernetes", "docker", "helm", "kafka", "grafana", "jenkins", "monitoring"]
        question_texts = [q["question"].lower() for q in questions]
        combined_text = " ".join(question_texts)
        
        # 최소 2개 이상의 DevOps 키워드가 포함되어야 함
        found_keywords = [keyword for keyword in devops_keywords if keyword in combined_text]
        assert len(found_keywords) >= 2, f"Expected DevOps keywords, found: {found_keywords}"

    @pytest.mark.asyncio
    async def test_multiple_question_generation_same_resume(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 같은 이력서로 여러 번 질문 생성
        Given: 같은 이력서 키가 주어지고
        When: 여러 번 면접 질문 생성을 요청하면
        Then: 매번 다른 질문들이 생성된다
        """
        # Given: 같은 이력서 키가 주어지고
        unique_key = "이민기_1"
        
        # When: 첫 번째 질문 생성을 요청하면
        response1 = await http_client.post(f"/interview/{unique_key}/questions")
        assert response1.status_code == 200
        
        # When: 두 번째 질문 생성을 요청하면
        response2 = await http_client.post(f"/interview/{unique_key}/questions")
        assert response2.status_code == 200
        
        # Then: 두 응답이 다른 질문들을 포함한다
        questions1 = [q["question"] for q in response1.json()["questions"]]
        questions2 = [q["question"] for q in response2.json()["questions"]]
        
        # 완전히 동일한 질문 세트가 아님을 확인
        assert questions1 != questions2, "Expected different questions for multiple generations"

    @pytest.mark.asyncio 
    async def test_interview_question_quality_validation(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 생성된 면접 질문의 품질 검증
        Given: 유효한 이력서가 주어지고
        When: 면접 질문을 생성하면
        Then: 질문들이 품질 기준을 만족한다
        """
        # Given: 유효한 이력서가 주어지고
        unique_key = "윤정은_1"
        
        # When: 면접 질문을 생성하면
        response = await http_client.post(f"/interview/{unique_key}/questions")
        assert response.status_code == 200
        
        result = response.json()
        questions = result["questions"]
        
        # Then: 질문들이 품질 기준을 만족한다
        for i, question in enumerate(questions):
            # 1. 질문이 충분히 구체적인지 (최소 20자 이상)
            assert len(question["question"]) >= 20, f"Question {i+1} too short: {question['question']}"
            
            # 2. 난이도가 유효한지
            assert question["difficulty"] in ["easy", "medium", "hard"], f"Invalid difficulty: {question['difficulty']}"
            
            # 3. 토픽이 설정되어 있는지
            assert len(question["topic"]) > 0, f"Missing topic for question {i+1}"
            
            # 4. 좋은 답변 가이드가 있는지 (what_good_answers_cover가 있다면)
            if "what_good_answers_cover" in question:
                assert len(question["what_good_answers_cover"]) > 0, f"Empty answer guide for question {i+1}"

    @pytest.mark.asyncio
    async def test_invalid_resume_key_handling(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 존재하지 않는 이력서 키로 요청
        Given: 존재하지 않는 이력서 키가 주어지고
        When: 면접 질문 생성을 요청하면
        Then: 404 에러가 반환된다
        """
        # Given: 존재하지 않는 이력서 키가 주어지고
        invalid_key = "존재하지않는키_999"
        
        # When: 면접 질문 생성을 요청하면
        response = await http_client.post(f"/interview/{invalid_key}/questions")
        
        # Then: 404 에러가 반환된다
        assert response.status_code == 404
        
        error_detail = response.json()
        assert "detail" in error_detail
        assert "not found" in error_detail["detail"].lower()
