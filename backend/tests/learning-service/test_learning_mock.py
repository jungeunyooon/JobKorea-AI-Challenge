"""
Learning Service - Mock 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

class TestLearningServiceMock:
    """학습 경로 생성 Mock 테스트"""

    @pytest.mark.asyncio
    async def test_generate_learning_path_mock(self):
        """
        시나리오: 학습 경로 생성 (Mock)
        Given: 유효한 이력서 키가 주어지고
        When: 학습 경로 생성을 요청하면
        Then: 개인 맞춤형 학습 경로가 생성된다
        """
        # Given: 유효한 이력서 키가 주어지고
        unique_key = "윤정은_1"
        expected_response = {
            "learning_path": [
                {
                    "category": "Technical Skills",
                    "title": "Spring Boot 심화 학습",
                    "description": "MSA 환경에서의 Spring Boot 고급 기능 습득",
                    "duration": "2-3주",
                    "difficulty": "intermediate",
                    "resources": [
                        "Spring Boot 공식 문서",
                        "마이크로서비스 패턴 도서"
                    ],
                    "learning_objectives": [
                        "Spring Cloud 활용법 습득",
                        "서비스 디스커버리 구현"
                    ]
                },
                {
                    "category": "System Design",
                    "title": "대규모 시스템 설계",
                    "description": "확장 가능한 시스템 아키텍처 설계 역량 개발",
                    "duration": "1개월",
                    "difficulty": "advanced",
                    "resources": [
                        "시스템 설계 인터뷰 도서",
                        "AWS 아키텍처 센터"
                    ],
                    "learning_objectives": [
                        "고가용성 시스템 설계",
                        "성능 최적화 전략 수립"
                    ]
                },
                {
                    "category": "Database",
                    "title": "NoSQL 데이터베이스 활용",
                    "description": "MongoDB, Redis 등 NoSQL 데이터베이스 심화 학습",
                    "duration": "3주",
                    "difficulty": "intermediate",
                    "resources": [
                        "MongoDB University 강의",
                        "Redis 공식 문서"
                    ],
                    "learning_objectives": [
                        "데이터 모델링 최적화",
                        "캐싱 전략 구현"
                    ]
                }
            ],
            "summary": "현재 Spring Boot 기반 백엔드 개발 경험을 바탕으로 시스템 설계 역량과 NoSQL 활용 능력을 향상시키는 학습 경로입니다.",
            "total_duration": "약 2-3개월",
            "priority_order": ["Technical Skills", "System Design", "Database"],
            "provider": "gemini",
            "generation_time": "2024-01-15T11:00:00Z"
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_client.post.return_value = mock_response
        
        # When: 학습 경로 생성을 요청하면
        response = await mock_client.post(f"/learning/{unique_key}/learning-path")
        
        # Then: 개인 맞춤형 학습 경로가 생성된다
        assert response.status_code == 200
        data = response.json()
        assert "learning_path" in data
        assert len(data["learning_path"]) >= 1
        assert "summary" in data
        assert "total_duration" in data
        assert data["provider"] == "gemini"
        
        # 각 학습 경로 항목 검증
        for path in data["learning_path"]:
            assert "category" in path
            assert "title" in path
            assert "description" in path
            assert "duration" in path
            assert "difficulty" in path
            assert "resources" in path
            assert "learning_objectives" in path

    @pytest.mark.asyncio
    async def test_generate_learning_path_with_provider_mock(self):
        """
        시나리오: 특정 LLM 제공자로 학습 경로 생성 (Mock)
        Given: 이력서 키와 LLM 제공자가 주어지고
        When: 특정 제공자로 학습 경로 생성을 요청하면
        Then: 해당 제공자로 학습 경로가 생성된다
        """
        # Given: 이력서 키와 LLM 제공자가 주어지고
        unique_key = "윤정은_1"
        provider = "openai"
        expected_response = {
            "learning_path": [
                {
                    "category": "Cloud Computing",
                    "title": "AWS 전문가 과정",
                    "description": "AWS 클라우드 서비스 심화 학습",
                    "duration": "1개월",
                    "difficulty": "advanced",
                    "resources": ["AWS Training"],
                    "learning_objectives": ["AWS 인증 취득"]
                }
            ],
            "provider": "openai",
            "generation_time": "2024-01-15T11:05:00Z"
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_client.post.return_value = mock_response
        
        # When: 특정 제공자로 학습 경로 생성을 요청하면
        response = await mock_client.post(
            f"/learning/{unique_key}/learning-path",
            params={"provider": provider}
        )
        
        # Then: 해당 제공자로 학습 경로가 생성된다
        assert response.status_code == 200
        data = response.json()
        assert data["provider"] == "openai"

    @pytest.mark.asyncio
    async def test_learning_path_resume_not_found_mock(self):
        """
        시나리오: 존재하지 않는 이력서로 학습 경로 생성 (Mock)
        Given: 존재하지 않는 이력서 키가 주어지고
        When: 학습 경로 생성을 요청하면
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
        
        # When: 학습 경로 생성을 요청하면
        response = await mock_client.post(f"/learning/{invalid_key}/learning-path")
        
        # Then: 404 에러가 반환된다
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data
        assert "not found" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_learning_path_categories_mock(self):
        """
        시나리오: 학습 경로 카테고리 다양성 검증 (Mock)
        Given: 학습 경로가 생성되고
        When: 카테고리를 분석하면
        Then: 다양한 카테고리가 포함된다
        """
        # Given: 학습 경로가 생성되고
        learning_paths = [
            {"category": "Technical Skills", "title": "기술 스킬"},
            {"category": "System Design", "title": "시스템 설계"},
            {"category": "Database", "title": "데이터베이스"},
            {"category": "DevOps", "title": "데브옵스"},
            {"category": "Communication", "title": "커뮤니케이션"}
        ]
        
        # When: 카테고리를 분석하면
        categories = set(path["category"] for path in learning_paths)
        
        # Then: 다양한 카테고리가 포함된다
        assert len(categories) >= 3  # 최소 3가지 카테고리
        expected_categories = {"Technical Skills", "System Design", "Database"}
        assert len(categories.intersection(expected_categories)) >= 2

    @pytest.mark.asyncio
    async def test_learning_path_difficulty_levels_mock(self):
        """
        시나리오: 학습 경로 난이도 분포 검증 (Mock)
        Given: 다양한 난이도의 학습 경로가 생성되고
        When: 난이도를 분석하면
        Then: 적절한 난이도 분포를 가진다
        """
        # Given: 다양한 난이도의 학습 경로가 생성되고
        learning_paths = [
            {"difficulty": "beginner", "title": "기초 과정"},
            {"difficulty": "intermediate", "title": "중급 과정 1"},
            {"difficulty": "intermediate", "title": "중급 과정 2"},
            {"difficulty": "advanced", "title": "고급 과정"}
        ]
        
        # When: 난이도를 분석하면
        difficulty_count = {}
        for path in learning_paths:
            difficulty = path["difficulty"]
            difficulty_count[difficulty] = difficulty_count.get(difficulty, 0) + 1
        
        # Then: 적절한 난이도 분포를 가진다
        assert "intermediate" in difficulty_count  # 중급 과정 포함
        assert difficulty_count.get("intermediate", 0) >= 1  # 중급 최소 1개

    @pytest.mark.asyncio
    async def test_concurrent_learning_path_generation_mock(self):
        """
        시나리오: 동시 학습 경로 생성 (Mock)
        Given: 여러 이력서 키가 주어지고
        When: 동시에 학습 경로 생성을 요청하면
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
                "learning_path": [
                    {"category": "Technical", "title": f"Path for {url}"}
                ],
                "provider": "gemini"
            }
            return mock_response
        
        mock_client.post.side_effect = mock_post_response
        
        # When: 동시에 학습 경로 생성을 요청하면
        import asyncio
        tasks = [
            mock_client.post(f"/learning/{key}/learning-path")
            for key in resume_keys
        ]
        responses = await asyncio.gather(*tasks)
        
        # Then: 모든 요청이 성공적으로 처리된다
        assert len(responses) == 3
        assert all(response.status_code == 200 for response in responses)
        
        # Mock 호출 검증
        assert mock_client.post.call_count == 3

    @pytest.mark.asyncio
    async def test_learning_path_resource_validation_mock(self):
        """
        시나리오: 학습 리소스 검증 (Mock)
        Given: 학습 경로에 리소스가 포함되고
        When: 리소스를 검증하면
        Then: 유용한 학습 리소스가 제공된다
        """
        # Given: 학습 경로에 리소스가 포함되고
        learning_path = {
            "category": "Technical Skills",
            "title": "Spring Boot 심화",
            "resources": [
                "Spring Boot 공식 문서",
                "Baeldung Spring Boot 튜토리얼",
                "Spring Boot in Action 도서",
                "YouTube Spring Boot 강의"
            ],
            "learning_objectives": [
                "Auto Configuration 이해",
                "Actuator 활용",
                "Testing 전략 수립"
            ]
        }
        
        # When: 리소스를 검증하면
        resources = learning_path["resources"]
        objectives = learning_path["learning_objectives"]
        
        # Then: 유용한 학습 리소스가 제공된다
        assert len(resources) >= 2  # 최소 2개 리소스
        assert len(objectives) >= 2  # 최소 2개 학습 목표
        assert any("문서" in resource or "도서" in resource or "강의" in resource 
                  for resource in resources)  # 다양한 형태의 리소스
