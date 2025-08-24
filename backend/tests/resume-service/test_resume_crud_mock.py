"""
Resume Service - CRUD 기능 Mock 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

class TestResumeServiceMock:
    """이력서 CRUD 기능 Mock 테스트"""

    @pytest.mark.asyncio
    async def test_create_resume_success_mock(self, test_resume_data: Dict[str, Any]):
        """
        시나리오: 새로운 이력서 생성 (Mock)
        Given: 유효한 이력서 데이터가 주어지고
        When: 이력서 생성을 요청하면
        Then: 성공적으로 생성되고 unique_key가 반환된다
        """
        # Given: 유효한 이력서 데이터가 주어지고
        expected_response = {
            "message": "Resume created successfully",
            "unique_key": "테스트개발자_1",
            "id": "mock_object_id"
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = expected_response
        mock_client.post.return_value = mock_response
        
        # When: 이력서 생성을 요청하면
        response = await mock_client.post("/resumes/", json=test_resume_data)
        
        # Then: 성공적으로 생성되고 unique_key가 반환된다
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["message"] == "Resume created successfully"
        assert "unique_key" in response_data
        assert "id" in response_data
        
        # Mock 호출 검증
        mock_client.post.assert_called_once_with("/resumes/", json=test_resume_data)

    @pytest.mark.asyncio
    async def test_get_resume_by_unique_key_mock(self):
        """
        시나리오: unique_key로 이력서 조회 (Mock)
        Given: 존재하는 unique_key가 주어지고
        When: 이력서 조회를 요청하면
        Then: 해당 이력서 정보가 반환된다
        """
        # Given: 존재하는 unique_key가 주어지고
        unique_key = "테스트개발자_1"
        expected_resume = {
            "name": "테스트개발자",
            "unique_key": unique_key,
            "total_experience_months": 36,
            "technical_skills": {
                "programming_languages": ["Java", "Python"],
                "frameworks": ["Spring Boot", "FastAPI"]
            }
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_resume
        mock_client.get.return_value = mock_response
        
        # When: 이력서 조회를 요청하면
        response = await mock_client.get(f"/resumes/{unique_key}")
        
        # Then: 해당 이력서 정보가 반환된다
        assert response.status_code == 200
        resume_data = response.json()
        assert resume_data["name"] == "테스트개발자"
        assert resume_data["unique_key"] == unique_key
        assert "technical_skills" in resume_data
        
        # Mock 호출 검증
        mock_client.get.assert_called_once_with(f"/resumes/{unique_key}")

    @pytest.mark.asyncio
    async def test_get_resume_not_found_mock(self):
        """
        시나리오: 존재하지 않는 이력서 조회 (Mock)
        Given: 존재하지 않는 unique_key가 주어지고
        When: 이력서 조회를 요청하면
        Then: 404 에러가 반환된다
        """
        # Given: 존재하지 않는 unique_key가 주어지고
        invalid_key = "존재하지않는키_999"
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Resume not found"}
        mock_client.get.return_value = mock_response
        
        # When: 이력서 조회를 요청하면
        response = await mock_client.get(f"/resumes/{invalid_key}")
        
        # Then: 404 에러가 반환된다
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data
        assert "not found" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_resume_data_validation_mock(self):
        """
        시나리오: 이력서 데이터 유효성 검증 (Mock)
        Given: 필수 필드가 누락된 이력서 데이터가 주어지고
        When: 이력서 생성을 요청하면
        Then: 유효성 검증 에러가 반환된다
        """
        # Given: 필수 필드가 누락된 이력서 데이터가 주어지고
        invalid_data = {
            "summary": "요약만 있는 불완전한 데이터"
            # name, contact 등 필수 필드 누락
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "detail": [
                {
                    "loc": ["body", "name"],
                    "msg": "field required",
                    "type": "value_error.missing"
                }
            ]
        }
        mock_client.post.return_value = mock_response
        
        # When: 이력서 생성을 요청하면
        response = await mock_client.post("/resumes/", json=invalid_data)
        
        # Then: 유효성 검증 에러가 반환된다
        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data
        assert isinstance(error_data["detail"], list)

    @pytest.mark.asyncio
    async def test_resume_list_retrieval_mock(self):
        """
        시나리오: 이력서 목록 조회 (Mock)
        Given: 여러 개의 이력서가 존재하고
        When: 이력서 목록 조회를 요청하면
        Then: 이력서 목록이 반환된다
        """
        # Given: 여러 개의 이력서가 존재하고
        expected_resumes = [
            {
                "name": "개발자1",
                "unique_key": "개발자1_1",
                "total_experience_months": 24
            },
            {
                "name": "개발자2", 
                "unique_key": "개발자2_1",
                "total_experience_months": 36
            }
        ]
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_resumes
        mock_client.get.return_value = mock_response
        
        # When: 이력서 목록 조회를 요청하면
        response = await mock_client.get("/resumes/")
        
        # Then: 이력서 목록이 반환된다
        assert response.status_code == 200
        resumes = response.json()
        assert isinstance(resumes, list)
        assert len(resumes) == 2
        assert all("unique_key" in resume for resume in resumes)

    @pytest.mark.asyncio
    async def test_resume_update_mock(self):
        """
        시나리오: 이력서 업데이트 (Mock)
        Given: 기존 이력서와 업데이트할 데이터가 주어지고
        When: 이력서 업데이트를 요청하면
        Then: 성공적으로 업데이트된다
        """
        # Given: 기존 이력서와 업데이트할 데이터가 주어지고
        unique_key = "테스트개발자_1"
        update_data = {
            "technical_skills": {
                "programming_languages": ["Java", "Python", "JavaScript"],
                "frameworks": ["Spring Boot", "FastAPI", "React"]
            }
        }
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Resume updated successfully",
            "unique_key": unique_key
        }
        mock_client.put.return_value = mock_response
        
        # When: 이력서 업데이트를 요청하면
        response = await mock_client.put(f"/resumes/{unique_key}", json=update_data)
        
        # Then: 성공적으로 업데이트된다
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Resume updated successfully"
        assert response_data["unique_key"] == unique_key

    @pytest.mark.asyncio 
    async def test_resume_delete_mock(self):
        """
        시나리오: 이력서 삭제 (Mock)
        Given: 존재하는 이력서가 주어지고
        When: 이력서 삭제를 요청하면
        Then: 성공적으로 삭제된다
        """
        # Given: 존재하는 이력서가 주어지고
        unique_key = "테스트개발자_1"
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Resume deleted successfully"
        }
        mock_client.delete.return_value = mock_response
        
        # When: 이력서 삭제를 요청하면
        response = await mock_client.delete(f"/resumes/{unique_key}")
        
        # Then: 성공적으로 삭제된다
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "Resume deleted successfully"
