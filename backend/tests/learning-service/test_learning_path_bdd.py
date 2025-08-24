"""
Learning Service - Given-When-Then 패턴 테스트 (장점/단점 분석 중심)
"""
import pytest
import httpx
from typing import Dict, Any

class TestLearningPathGenerationBDD:
    """장점/단점 체계적 분석 기반 학습 경로 생성 테스트"""

    @pytest.mark.asyncio
    async def test_generate_learning_path_with_analysis(
        self, 
        http_client: httpx.AsyncClient,
        existing_resume_keys: list
    ):
        """
        시나리오: 장점/단점 분석 기반 학습 경로 생성
        Given: 유효한 이력서가 주어지고
        When: 학습 경로 생성을 요청하면
        Then: 장점/단점 분석과 함께 학습 경로가 생성된다
        """
        # Given: 유효한 이력서가 주어지고
        unique_key = existing_resume_keys[0]  # 윤정은_1
        
        # When: 학습 경로 생성을 요청하면
        response = await http_client.post(f"/learning/{unique_key}/learning-path")
        
        # Then: 장점/단점 분석과 함께 학습 경로가 생성된다
        assert response.status_code == 200
        
        result = response.json()
        
        # 기본 응답 구조 검증
        assert "analysis" in result
        assert "summary" in result
        assert "learning_paths" in result
        assert "provider" in result
        assert result["provider"] == "gemini"
        
        # 장점/단점 분석 구조 검증
        analysis = result["analysis"]
        assert "strengths" in analysis
        assert "weaknesses" in analysis
        assert isinstance(analysis["strengths"], list)
        assert isinstance(analysis["weaknesses"], list)
        assert len(analysis["strengths"]) > 0
        assert len(analysis["weaknesses"]) > 0
        
        # 학습 경로 구조 검증
        learning_paths = result["learning_paths"]
        assert isinstance(learning_paths, list)
        assert len(learning_paths) == 5  # 5개 학습 경로
        
        for path in learning_paths:
            assert "type" in path
            assert path["type"] in ["strength", "weakness"]
            assert "title" in path
            assert "description" in path
            assert "reason" in path
            assert "resources" in path
            assert "link" in path

    @pytest.mark.asyncio
    async def test_strength_weakness_balance_validation(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 강점 심화와 약점 보완의 균형 검증
        Given: DevOps 전문가 이력서가 주어지고
        When: 학습 경로를 생성하면
        Then: 강점 심화와 약점 보완이 균형있게 제안된다
        """
        # Given: DevOps 전문가 이력서가 주어지고
        unique_key = "라이언_1"
        
        # When: 학습 경로를 생성하면
        response = await http_client.post(f"/learning/{unique_key}/learning-path")
        assert response.status_code == 200
        
        result = response.json()
        learning_paths = result["learning_paths"]
        
        # Then: 강점 심화와 약점 보완이 균형있게 제안된다
        strength_paths = [p for p in learning_paths if p["type"] == "strength"]
        weakness_paths = [p for p in learning_paths if p["type"] == "weakness"]
        
        # 강점과 약점 학습 경로가 모두 존재해야 함
        assert len(strength_paths) > 0, "No strength-focused learning paths found"
        assert len(weakness_paths) > 0, "No weakness-focused learning paths found"
        
        # 비율이 극단적이지 않아야 함 (최소 20% 이상)
        strength_ratio = len(strength_paths) / len(learning_paths)
        weakness_ratio = len(weakness_paths) / len(learning_paths)
        
        assert strength_ratio >= 0.2, f"Too few strength paths: {strength_ratio:.1%}"
        assert weakness_ratio >= 0.2, f"Too few weakness paths: {weakness_ratio:.1%}"

    @pytest.mark.asyncio
    async def test_personalized_reasoning_quality(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 개인맞춤형 제시 이유의 품질 검증
        Given: 유효한 이력서가 주어지고
        When: 학습 경로를 생성하면
        Then: 각 학습 경로에 구체적인 개인맞춤 이유가 포함된다
        """
        # Given: 인턴 경험이 있는 개발자 이력서가 주어지고
        unique_key = "이민기_1"
        
        # When: 학습 경로를 생성하면
        response = await http_client.post(f"/learning/{unique_key}/learning-path")
        assert response.status_code == 200
        
        result = response.json()
        learning_paths = result["learning_paths"]
        
        # Then: 각 학습 경로에 구체적인 개인맞춤 이유가 포함된다
        for i, path in enumerate(learning_paths):
            reason = path["reason"]
            
            # 이유가 충분히 구체적인지 (최소 15자)
            assert len(reason) >= 15, f"Path {i+1} reason too short: {reason}"
            
            # 강점/약점 유형에 맞는 키워드가 포함되는지
            if path["type"] == "strength":
                strength_keywords = ["경험", "활용", "심화", "전문성", "강점", "바탕"]
                assert any(keyword in reason for keyword in strength_keywords), f"Strength path {i+1} lacks strength reasoning: {reason}"
            
            elif path["type"] == "weakness":
                weakness_keywords = ["부족", "보완", "필요", "개선", "강화", "역량"]
                assert any(keyword in reason for keyword in weakness_keywords), f"Weakness path {i+1} lacks weakness reasoning: {reason}"

    @pytest.mark.asyncio
    async def test_learning_path_links_validation(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 학습 리소스 링크의 유효성 검증
        Given: 유효한 이력서가 주어지고
        When: 학습 경로를 생성하면
        Then: 실제 학습 리소스 링크가 제공된다
        """
        # Given: 유효한 이력서가 주어지고
        unique_key = "윤정은_1"
        
        # When: 학습 경로를 생성하면
        response = await http_client.post(f"/learning/{unique_key}/learning-path")
        assert response.status_code == 200
        
        result = response.json()
        learning_paths = result["learning_paths"]
        
        # Then: 실제 학습 리소스 링크가 제공된다
        for i, path in enumerate(learning_paths):
            link = path["link"]
            
            # 링크가 유효한 URL 형식인지
            assert link.startswith(("http://", "https://")), f"Path {i+1} invalid link format: {link}"
            
            # 일반적인 링크가 아닌 구체적인 링크인지 (google.com 금지)
            forbidden_links = ["google.com", "www.google.com"]
            assert not any(forbidden in link for forbidden in forbidden_links), f"Path {i+1} uses generic link: {link}"
            
            # 리소스 목록이 있는지
            resources = path["resources"]
            assert isinstance(resources, list), f"Path {i+1} resources not a list"
            assert len(resources) > 0, f"Path {i+1} has no resources"

    @pytest.mark.asyncio
    async def test_technical_depth_by_experience_level(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 경력 수준에 따른 기술적 깊이 검증
        Given: 다양한 경력 수준의 이력서가 주어지고
        When: 학습 경로를 생성하면
        Then: 경력에 적합한 기술적 깊이의 학습이 제안된다
        """
        # DevOps 전문가 (14개월) vs 일반 백엔드 (4개월)
        test_cases = [
            ("라이언_1", "high"),  # DevOps 전문가 - 높은 깊이 기대
            ("윤정은_1", "medium")  # 4개월 경력 - 중간 깊이 기대
        ]
        
        for unique_key, expected_depth in test_cases:
            # When: 학습 경로를 생성하면
            response = await http_client.post(f"/learning/{unique_key}/learning-path")
            assert response.status_code == 200
            
            result = response.json()
            learning_paths = result["learning_paths"]
            
            # Then: 경력에 적합한 기술적 깊이가 반영된다
            all_titles = " ".join([path["title"] for path in learning_paths])
            all_descriptions = " ".join([path["description"] for path in learning_paths])
            combined_text = (all_titles + " " + all_descriptions).lower()
            
            if expected_depth == "high":
                # 고급 키워드가 포함되어야 함
                advanced_keywords = ["아키텍처", "최적화", "고급", "심화", "전문", "확장", "설계"]
                found_advanced = [kw for kw in advanced_keywords if kw in combined_text]
                assert len(found_advanced) >= 2, f"Expected advanced keywords for {unique_key}, found: {found_advanced}"
            
            elif expected_depth == "medium":
                # 기본-중급 키워드가 적절히 포함되어야 함
                basic_keywords = ["기본", "입문", "학습", "이해", "구현", "활용"]
                found_basic = [kw for kw in basic_keywords if kw in combined_text]
                assert len(found_basic) >= 1, f"Expected basic-medium keywords for {unique_key}, found: {found_basic}"

    @pytest.mark.asyncio
    async def test_multiple_generation_diversity(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 다중 생성 시 다양성 검증
        Given: 같은 이력서로
        When: 여러 번 학습 경로를 생성하면
        Then: 다양한 학습 방향이 제시된다
        """
        # Given: 같은 이력서로
        unique_key = "이민기_1"
        
        # When: 두 번의 학습 경로를 생성하면
        response1 = await http_client.post(f"/learning/{unique_key}/learning-path")
        assert response1.status_code == 200
        
        response2 = await http_client.post(f"/learning/{unique_key}/learning-path")
        assert response2.status_code == 200
        
        # Then: 다양한 학습 방향이 제시된다
        paths1 = response1.json()["learning_paths"]
        paths2 = response2.json()["learning_paths"]
        
        titles1 = {path["title"] for path in paths1}
        titles2 = {path["title"] for path in paths2}
        
        # 완전히 동일하지 않아야 함 (최소 1개는 달라야 함)
        overlap = len(titles1.intersection(titles2))
        total_unique = len(titles1.union(titles2))
        
        assert overlap < len(titles1), f"Too much overlap between generations: {overlap}/{len(titles1)}"
