"""
Resume Service - CRUD 기능 테스트
"""
import pytest
import httpx
from typing import Dict, Any

class TestResumeServiceBDD:
    """이력서 CRUD 기능 Given-When-Then 테스트"""

    @pytest.mark.asyncio
    async def test_create_resume_success(
        self, 
        http_client: httpx.AsyncClient,
        test_resume_data: Dict[str, Any]
    ):
        """
        시나리오: 새로운 이력서 생성
        Given: 유효한 이력서 데이터가 주어지고
        When: 이력서 생성을 요청하면
        Then: 성공적으로 이력서가 생성된다
        """
        # Given: 유효한 이력서 데이터가 주어지고
        resume_data = test_resume_data.copy()
        import uuid
        resume_data["name"] = f"테스트사용자_{uuid.uuid4().hex[:8]}"  # 고유한 이름
        
        # When: 이력서 생성을 요청하면
        response = await http_client.post("/resumes/", json=resume_data)
        
        # Then: 성공적으로 이력서가 생성된다
        assert response.status_code == 200
        
        result = response.json()
        assert "message" in result
        assert "resume_id" in result
        assert "unique_key" in result
        assert result["message"] == "Resume created successfully"
        assert result["unique_key"].startswith(resume_data["name"])

    @pytest.mark.asyncio
    async def test_get_resume_by_unique_key(
        self, 
        http_client: httpx.AsyncClient,
        existing_resume_keys: list
    ):
        """
        시나리오: unique_key로 이력서 조회
        Given: 기존에 생성된 이력서가 있고
        When: unique_key로 조회를 요청하면
        Then: 해당 이력서 정보가 반환된다
        """
        # Given: 기존에 생성된 이력서가 있고
        unique_key = existing_resume_keys[0]  # 윤정은_1
        
        # When: unique_key로 조회를 요청하면
        response = await http_client.get(f"/resumes/{unique_key}")
        
        # Then: 해당 이력서 정보가 반환된다
        assert response.status_code == 200
        
        result = response.json()
        assert "name" in result
        assert "unique_key" in result
        assert result["unique_key"] == unique_key

    @pytest.mark.parametrize("invalid_key", [
        "존재하지않는키_999",
        "",
        "invalid/key/format",
        "너무긴키_" + "x" * 100
    ])
    @pytest.mark.asyncio
    async def test_get_resume_invalid_keys(
        self, 
        http_client: httpx.AsyncClient,
        invalid_key: str
    ):
        """
        시나리오: 잘못된 키로 이력서 조회
        Given: 잘못된 unique_key가 주어지고
        When: 이력서 조회를 요청하면
        Then: 적절한 에러가 반환된다
        """
        # Given: 잘못된 unique_key가 주어지고
        # When: 이력서 조회를 요청하면
        response = await http_client.get(f"/resumes/{invalid_key}")
        
        # Then: 적절한 에러가 반환된다
        if invalid_key == "":
            assert response.status_code == 404  # Empty path
        else:
            assert response.status_code in [404, 422]  # Not found or validation error

    @pytest.mark.asyncio
    async def test_resume_data_validation(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 이력서 데이터 유효성 검증
        Given: 필수 필드가 누락된 이력서 데이터가 주어지고
        When: 이력서 생성을 요청하면
        Then: 유효성 검증 에러가 반환된다
        """
        # Given: 필수 필드가 누락된 이력서 데이터가 주어지고
        invalid_data = {
            "summary": "요약만 있는 불완전한 데이터"
            # name, contact 등 필수 필드 누락
        }
        
        # When: 이력서 생성을 요청하면
        response = await http_client.post("/resumes/", json=invalid_data)
        
        # Then: 유효성 검증 에러가 반환된다
        assert response.status_code == 422
        
        error_detail = response.json()
        assert "detail" in error_detail

    @pytest.mark.asyncio
    async def test_resume_list_retrieval(
        self, 
        http_client: httpx.AsyncClient
    ):
        """
        시나리오: 이력서 목록 조회
        Given: 여러 개의 이력서가 존재하고
        When: 이력서 목록 조회를 요청하면
        Then: 이력서 목록이 반환된다
        """
        # Given: 여러 개의 이력서가 존재하고 (기존 데이터 활용)
        # When: 이력서 목록 조회를 요청하면
        response = await http_client.get("/resumes/")
        
        # Then: 이력서 목록이 반환된다
        assert response.status_code == 200
        
        result = response.json()
        assert isinstance(result, list)
        assert len(result) > 0  # 최소 하나의 이력서는 존재해야 함
        
        # 각 이력서 항목이 필수 정보를 포함하는지 확인
        for resume in result:
            assert "unique_key" in resume
            assert "name" in resume
            assert "created_at" in resume
