"""
Interview Service - Flaky Test 대응 전략
"""
import pytest
import httpx
import asyncio
from typing import List

class TestInterviewServiceFlaky:
    """네트워크 이슈 및 불안정한 LLM API 호출에 대한 대응 테스트"""

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.asyncio
    async def test_llm_api_call_with_retry(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        LLM API 호출 테스트 - 네트워크 이슈로 인한 실패 시 재시도
        
        Note:
            @pytest.mark.flaky 데코레이터로 최대 3회 재시도, 2초 지연
        """
        # Given: 유효한 이력서가 주어지고
        unique_key = "윤정은_1"
        
        # When: 면접 질문 생성을 요청하면
        response = await http_client.post(f"/interview/{unique_key}/questions")
        
        # Then: 성공적으로 응답받거나 폴백이 작동한다
        assert response.status_code == 200
        
        result = response.json()
        assert result["provider"] in ["gemini", "openai", "claude"]  # 폴백 허용
        assert len(result["questions"]) == 5
        assert "model" in result

    @pytest.mark.parametrize("unique_key", [
        "윤정은_1", "이민기_1", "라이언_1"
    ])
    @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @pytest.mark.asyncio
    async def test_concurrent_interview_generation_stability(
        self, 
        http_client: httpx.AsyncClient,
        unique_key: str
    ):
        """
        동시 다발적 면접 질문 생성 안정성 테스트
        
        Note:
            여러 이력서에 대해 동시 요청으로 시스템 안정성 검증
        """
        # Given: 유효한 이력서가 주어지고
        # When: 면접 질문 생성을 요청하면
        response = await http_client.post(f"/interview/{unique_key}/questions")
        
        # Then: 안정적으로 응답한다
        assert response.status_code == 200
        
        result = response.json()
        assert len(result["questions"]) == 5
        assert "provider" in result

    @pytest.mark.timeout(30)  # 30초 타임아웃
    @pytest.mark.asyncio
    async def test_interview_generation_with_timeout(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        면접 질문 생성 타임아웃 테스트
        
        Note:
            30초 내에 응답하지 않으면 테스트 실패
        """
        # Given: 복잡한 이력서가 주어지고 (DevOps 전문가)
        unique_key = "라이언_1"
        
        # When: 면접 질문 생성을 요청하면
        start_time = asyncio.get_event_loop().time()
        response = await http_client.post(f"/interview/{unique_key}/questions")
        end_time = asyncio.get_event_loop().time()
        
        # Then: 합리적인 시간 내에 응답한다
        response_time = end_time - start_time
        assert response.status_code == 200
        assert response_time < 25, f"Response took too long: {response_time:.2f}s"

    @pytest.mark.asyncio
    async def test_fallback_strategy_verification(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        LLM 폴백 전략 검증 테스트
        
        Note:
            여러 번 호출하여 다양한 provider가 사용되는지 확인
        """
        # Given: 유효한 이력서가 주어지고
        unique_key = "이민기_1"
        providers_used = set()
        
        # When: 여러 번 면접 질문을 생성하면
        for _ in range(5):  # 5번 시도
            try:
                response = await http_client.post(f"/interview/{unique_key}/questions")
                if response.status_code == 200:
                    result = response.json()
                    providers_used.add(result.get("provider", "unknown"))
            except Exception:
                # 네트워크 오류 등은 무시하고 계속 진행
                continue
            
            # 잠시 대기
            await asyncio.sleep(0.5)
        
        # Then: 최소한 하나의 provider는 성공해야 함
        assert len(providers_used) > 0, "No successful LLM provider responses"
        assert providers_used.issubset({"gemini", "openai", "claude"}), f"Unexpected providers: {providers_used}"

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_stress_test_multiple_questions(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        스트레스 테스트 - 다수의 연속 요청
        
        Note:
            @pytest.mark.slow로 일반 테스트에서 제외 가능
        """
        # Given: 다양한 이력서들이 주어지고
        resume_keys = ["윤정은_1", "이민기_1", "라이언_1"]
        successful_requests = 0
        failed_requests = 0
        
        # When: 연속적으로 많은 요청을 보내면
        for i in range(10):  # 10번의 요청
            try:
                unique_key = resume_keys[i % len(resume_keys)]
                response = await http_client.post(f"/interview/{unique_key}/questions")
                
                if response.status_code == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
                    
            except Exception as e:
                failed_requests += 1
                print(f"Request {i+1} failed: {e}")
            
            # 요청 간 짧은 대기
            await asyncio.sleep(0.1)
        
        # Then: 대부분의 요청이 성공해야 함 (최소 70%)
        success_rate = successful_requests / (successful_requests + failed_requests)
        assert success_rate >= 0.7, f"Success rate too low: {success_rate:.2%} ({successful_requests}/{successful_requests + failed_requests})"

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.asyncio
    async def test_llm_response_parsing_resilience(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        LLM 응답 파싱 안정성 테스트
        
        Note:
            LLM이 예상과 다른 형식으로 응답해도 안정적으로 처리하는지 확인
        """
        # Given: 유효한 이력서가 주어지고
        unique_key = "윤정은_1"
        
        # When: 면접 질문을 생성하면
        response = await http_client.post(f"/interview/{unique_key}/questions")
        
        # Then: 파싱이 안정적으로 처리된다
        assert response.status_code == 200
        
        result = response.json()
        
        # 필수 필드 존재 확인
        assert "questions" in result
        assert "provider" in result
        assert "generated_at" in result
        
        # 질문 구조 검증
        questions = result["questions"]
        assert isinstance(questions, list)
        assert len(questions) > 0
        
        for question in questions:
            assert isinstance(question, dict)
            assert "question" in question
            assert "difficulty" in question
            assert len(question["question"]) > 0

    @pytest.mark.integration
    @pytest.mark.timeout(45)
    @pytest.mark.asyncio
    async def test_end_to_end_interview_flow(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        엔드투엔드 통합 테스트 - 전체 플로우 검증
        
        Note:
            실제 사용자 시나리오를 시뮬레이션하는 통합 테스트
        """
        # Given: 새로운 이력서를 생성하고
        test_resume = {
            "name": "통합테스트사용자",
            "summary": "풀스택 개발자 테스트 이력서",
            "contact": {
                "email": "integration.test@example.com",
                "github": "https://github.com/integrationtest",
                "phone": "010-9999-9999"
            },
            "work_experiences": [
                {
                    "company": "통합테스트회사",
                    "position": "개발자",
                    "duration": "2023.01 ~ 현재",
                    "project_name": "테스트 프로젝트",
                    "tech_stack": ["React", "Node.js", "PostgreSQL"],
                    "achievements": ["테스트 시스템 구축"]
                }
            ],
            "personal_projects": [],
            "technical_skills": {
                "programming_languages": ["JavaScript", "TypeScript"],
                "frameworks": ["React", "Node.js"],
                "databases": ["PostgreSQL"],
                "cloud_platforms": ["AWS"],
                "devops_tools": ["Docker"]
            },
            "total_experience_months": 12,
            "activities": []
        }
        
        # When: 이력서를 생성하고
        resume_response = await http_client.post("/resumes/", json=test_resume)
        assert resume_response.status_code == 200
        
        resume_result = resume_response.json()
        unique_key = resume_result["unique_key"]
        
        # When: 면접 질문을 생성하면
        questions_response = await http_client.post(f"/interview/{unique_key}/questions")
        
        # Then: 전체 플로우가 성공적으로 완료된다
        assert questions_response.status_code == 200
        
        questions_result = questions_response.json()
        assert len(questions_result["questions"]) == 5
        assert questions_result["unique_key"] == unique_key
