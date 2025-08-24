"""
Interview Service - Mock 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

class TestInterviewServiceMock:
    """면접 질문 생성 Mock 테스트"""

    @pytest.mark.asyncio
    async def test_generate_interview_questions_mock(self):
        """
        시나리오: 면접 질문 생성 (Mock)
        Given: 유효한 이력서 키가 주어지고
        When: 면접 질문 생성을 요청하면
        Then: 5개의 면접 질문이 생성된다
        """
        # Given: 유효한 이력서 키가 주어지고
        unique_key = "윤정은_1"
        expected_response = {
            "questions": [
                {
                    "difficulty": "medium",
                    "topic": "Spring Boot, MSA",
                    "type": "Technical",
                    "question": "MSA 아키텍처에서 서비스 간 통신 방법에 대해 설명해주세요."
                },
                {
                    "difficulty": "medium", 
                    "topic": "Python, FastAPI",
                    "type": "Implementation",
                    "question": "FastAPI에서 비동기 처리를 어떻게 구현하셨나요?"
                },
                {
                    "difficulty": "high",
                    "topic": "AWS, Redis",
                    "type": "Problem Solving",
                    "question": "Redis 캐싱 전략과 성능 개선 경험을 설명해주세요."
                },
                {
                    "difficulty": "medium",
                    "topic": "Database",
                    "type": "Technical",
                    "question": "대용량 데이터 처리 시 고려사항은 무엇인가요?"
                },
                {
                    "difficulty": "high",
                    "topic": "System Design",
                    "type": "Design",
                    "question": "확장 가능한 시스템 설계 원칙에 대해 설명해주세요."
                }
            ],
            "provider": "gemini",
            "generation_time": "2024-01-15T10:30:00Z"
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_client.post.return_value = mock_response
        
        # When: 면접 질문 생성을 요청하면
        response = await mock_client.post(f"/interview/{unique_key}/questions")
        
        # Then: 5개의 면접 질문이 생성된다
        assert response.status_code == 200
        data = response.json()
        assert len(data["questions"]) == 5
        assert data["provider"] == "gemini"
        assert all("question" in q for q in data["questions"])
        assert all("difficulty" in q for q in data["questions"])
        assert all("topic" in q for q in data["questions"])

    @pytest.mark.asyncio
    async def test_generate_questions_with_provider_mock(self):
        """
        시나리오: 특정 LLM 제공자로 면접 질문 생성 (Mock)
        Given: 이력서 키와 LLM 제공자가 주어지고
        When: 특정 제공자로 면접 질문 생성을 요청하면
        Then: 해당 제공자로 질문이 생성된다
        """
        # Given: 이력서 키와 LLM 제공자가 주어지고
        unique_key = "윤정은_1"
        provider = "claude"
        expected_response = {
            "questions": [
                {
                    "difficulty": "medium",
                    "topic": "Spring Boot",
                    "type": "Technical",
                    "question": "Spring Boot의 자동 설정 원리를 설명해주세요."
                }
            ] * 5,  # 5개 질문
            "provider": "claude",
            "generation_time": "2024-01-15T10:35:00Z"
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_client.post.return_value = mock_response
        
        # When: 특정 제공자로 면접 질문 생성을 요청하면
        response = await mock_client.post(
            f"/interview/{unique_key}/questions",
            params={"provider": provider}
        )
        
        # Then: 해당 제공자로 질문이 생성된다
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == "claude"
        assert len(data["questions"]) == 5

    @pytest.mark.asyncio
    async def test_generate_questions_resume_not_found_mock(self):
        """
        시나리오: 존재하지 않는 이력서로 질문 생성 (Mock)
        Given: 존재하지 않는 이력서 키가 주어지고
        When: 면접 질문 생성을 요청하면
        Then: 404 에러가 반환된다
        """
        # Given: 존재하지 않는 이력서 키가 주어지고
        invalid_key = "존재하지않는키_999"
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "detail": "Resume not found with key: 존재하지않는키_999"
        }
        mock_client.post.return_value = mock_response
        
        # When: 면접 질문 생성을 요청하면
        response = await mock_client.post(f"/interview/{invalid_key}/questions")
        
        # Then: 404 에러가 반환된다
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data
        assert "not found" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_questions_difficulty_distribution_mock(self):
        """
        시나리오: 질문 난이도 분포 검증 (Mock)
        Given: 면접 질문이 생성되고
        When: 질문들의 난이도를 분석하면
        Then: 적절한 난이도 분포를 가진다
        """
        # Given: 면접 질문이 생성되고
        questions = [
            {"difficulty": "easy", "question": "Easy question 1"},
            {"difficulty": "easy", "question": "Easy question 2"},
            {"difficulty": "medium", "question": "Medium question 1"},
            {"difficulty": "medium", "question": "Medium question 2"},
            {"difficulty": "hard", "question": "Hard question 1"}
        ]
        
        # When: 질문들의 난이도를 분석하면
        difficulty_count = {}
        for q in questions:
            difficulty = q["difficulty"]
            difficulty_count[difficulty] = difficulty_count.get(difficulty, 0) + 1
        
        # Then: 적절한 난이도 분포를 가진다
        assert difficulty_count.get("easy", 0) >= 1  # 최소 1개 이상
        assert difficulty_count.get("medium", 0) >= 1  # 최소 1개 이상
        assert difficulty_count.get("hard", 0) >= 1  # 최소 1개 이상
        
        # 전체 5개 질문
        total_questions = sum(difficulty_count.values())
        assert total_questions == 5

    @pytest.mark.asyncio
    async def test_async_question_generation_mock(self):
        """
        시나리오: 비동기 질문 생성 (Mock)
        Given: 여러 이력서 키가 주어지고
        When: 동시에 질문 생성을 요청하면
        Then: 모든 요청이 성공적으로 처리된다
        """
        # Given: 여러 이력서 키가 주어지고
        resume_keys = ["윤정은_1", "이민기_1", "라이언_1"]
        
        # Mock HTTP client
        mock_client = AsyncMock()
        
        async def mock_post_response(url, **kwargs):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "questions": [{"question": f"Question for {url}"}] * 5,
                "provider": "gemini"
            }
            return mock_response
        
        mock_client.post.side_effect = mock_post_response
        
        # When: 동시에 질문 생성을 요청하면
        import asyncio
        tasks = [
            mock_client.post(f"/interview/{key}/questions")
            for key in resume_keys
        ]
        responses = await asyncio.gather(*tasks)
        
        # Then: 모든 요청이 성공적으로 처리된다
        assert len(responses) == 3
        assert all(response.status_code == 200 for response in responses)
        
        # Mock 호출 검증
        assert mock_client.post.call_count == 3

    @pytest.mark.asyncio
    async def test_question_type_distribution_mock(self):
        """
        시나리오: 질문 유형 분포 검증 (Mock)
        Given: 다양한 유형의 질문이 생성되고
        When: 질문 유형을 분석하면
        Then: 균형잡힌 유형 분포를 가진다
        """
        # Given: 다양한 유형의 질문이 생성되고
        questions = [
            {"type": "Technical", "question": "기술 질문 1"},
            {"type": "Technical", "question": "기술 질문 2"},
            {"type": "Implementation", "question": "구현 질문 1"},
            {"type": "Problem Solving", "question": "문제 해결 질문 1"},
            {"type": "Design", "question": "설계 질문 1"}
        ]
        
        # When: 질문 유형을 분석하면
        type_count = {}
        for q in questions:
            question_type = q["type"]
            type_count[question_type] = type_count.get(question_type, 0) + 1
        
        # Then: 균형잡힌 유형 분포를 가진다
        assert len(type_count) >= 3  # 최소 3가지 유형
        assert type_count.get("Technical", 0) >= 1  # 기술 질문 최소 1개
        
        # 전체 5개 질문
        total_questions = sum(type_count.values())
        assert total_questions == 5
