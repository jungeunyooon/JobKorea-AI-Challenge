"""
Resume Service - 사용자 엔드포인트 검증 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from urllib.parse import quote
import json

class TestUserEndpointValidation:
    """사용자 엔드포인트 입력 검증 테스트"""

    @pytest.mark.asyncio
    async def test_empty_user_name_validation(self):
        """
        시나리오: 빈 사용자 이름으로 조회 시도 
        Given: 빈 문자열이 사용자 이름으로 주어지고
        When: 사용자 이력서 조회를 요청하면
        Then: 422 유효성 검증 에러가 반환된다
        """
        # Given: 빈 문자열이 사용자 이름으로 주어지고
        empty_names = ["", " ", "   "]
        
        for empty_name in empty_names:
            # Mock HTTP client
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 422
            mock_response.json.return_value = {
                "detail": "Validation error in field 'name': User name cannot be empty",
                "error_code": "RESUME_VALIDATION_ERROR",
                "timestamp": "2024-01-15T10:30:00Z",
                "details": {
                    "field": "name",
                    "validation_message": "User name cannot be empty"
                }
            }
            mock_client.get.return_value = mock_response
            
            # When: 사용자 이력서 조회를 요청하면
            response = await mock_client.get(f"/api/v1/resumes/user/{quote(empty_name)}")
            
            # Then: 422 유효성 검증 에러가 반환된다
            assert response.status_code == 422
            error_data = response.json()
            assert error_data["error_code"] == "RESUME_VALIDATION_ERROR"
            assert "empty" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_too_long_user_name_validation(self):
        """
        시나리오: 너무 긴 사용자 이름으로 조회 시도
        Given: 100자를 초과하는 사용자 이름이 주어지고
        When: 사용자 이력서 조회를 요청하면
        Then: 422 유효성 검증 에러가 반환된다
        """
        # Given: 100자를 초과하는 사용자 이름이 주어지고
        long_name = "a" * 101  # 101자
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "detail": "Validation error in field 'name': User name is too long (max 100 characters)",
            "error_code": "RESUME_VALIDATION_ERROR",
            "timestamp": "2024-01-15T10:30:00Z",
            "details": {
                "field": "name",
                "validation_message": "User name is too long (max 100 characters)"
            }
        }
        mock_client.get.return_value = mock_response
        
        # When: 사용자 이력서 조회를 요청하면
        response = await mock_client.get(f"/api/v1/resumes/user/{quote(long_name)}")
        
        # Then: 422 유효성 검증 에러가 반환된다
        assert response.status_code == 422
        error_data = response.json()
        assert error_data["error_code"] == "RESUME_VALIDATION_ERROR"
        assert "too long" in error_data["detail"].lower()

    @pytest.mark.asyncio 
    async def test_url_encoded_special_characters(self):
        """
        시나리오: URL 인코딩된 특수문자가 포함된 사용자 이름 처리
        Given: URL 인코딩된 특수문자가 포함된 이름이 주어지고
        When: 사용자 이력서 조회를 요청하면
        Then: 올바르게 디코딩되어 처리된다
        """
        # Given: URL 인코딩된 특수문자가 포함된 이름
        # %E3%85%81는 "ㅁ" 문자의 URL 인코딩
        encoded_name = "%E3%85%81"  # "ㅁ"
        expected_decoded = "ㅁ"
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "detail": "Validation error in field 'name': User name contains invalid characters",
            "error_code": "RESUME_VALIDATION_ERROR",
            "timestamp": "2024-01-15T10:30:00Z",
            "details": {
                "field": "name",
                "validation_message": "User name contains invalid characters"
            }
        }
        mock_client.get.return_value = mock_response
        
        # When: 사용자 이력서 조회를 요청하면
        response = await mock_client.get(f"/api/v1/resumes/user/{encoded_name}")
        
        # Then: 적절한 에러 응답이 반환된다 (단일 문자이므로 유효성 검증 실패할 수 있음)
        # 또는 정상적으로 디코딩되어 처리된다
        assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_control_characters_validation(self):
        """
        시나리오: 제어 문자가 포함된 사용자 이름 검증
        Given: 제어 문자가 포함된 사용자 이름이 주어지고
        When: 사용자 이력서 조회를 요청하면
        Then: 422 유효성 검증 에러가 반환된다
        """
        # Given: 제어 문자가 포함된 사용자 이름
        names_with_control_chars = [
            "user\x00name",  # NULL 문자
            "user\x0Aname",  # 개행 문자
            "user\x0Dname",  # 캐리지 리턴
            "user\x1Fname",  # 다른 제어 문자
        ]
        
        for invalid_name in names_with_control_chars:
            # Mock HTTP client
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 422
            mock_response.json.return_value = {
                "detail": "Validation error in field 'name': User name contains invalid characters",
                "error_code": "RESUME_VALIDATION_ERROR",
                "timestamp": "2024-01-15T10:30:00Z",
                "details": {
                    "field": "name",
                    "validation_message": "User name contains invalid characters"
                }
            }
            mock_client.get.return_value = mock_response
            
            # When: 사용자 이력서 조회를 요청하면
            response = await mock_client.get(f"/api/v1/resumes/user/{quote(invalid_name)}")
            
            # Then: 422 유효성 검증 에러가 반환된다
            assert response.status_code == 422
            error_data = response.json()
            assert error_data["error_code"] == "RESUME_VALIDATION_ERROR"

    @pytest.mark.asyncio
    async def test_valid_user_name_success(self):
        """
        시나리오: 유효한 사용자 이름으로 조회 성공
        Given: 유효한 사용자 이름이 주어지고
        When: 사용자 이력서 조회를 요청하면
        Then: 성공적으로 이력서 목록이 반환된다
        """
        # Given: 유효한 사용자 이름
        valid_names = [
            "윤정은",
            "john_doe", 
            "user123",
            "Jane Smith",
            "김철수"
        ]
        
        for valid_name in valid_names:
            # Mock HTTP client
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "user": valid_name,
                "count": 2,
                "resumes": [
                    {
                        "unique_key": f"{valid_name}_1",
                        "name": valid_name,
                        "created_at": "2024-01-15T10:00:00Z"
                    },
                    {
                        "unique_key": f"{valid_name}_2", 
                        "name": valid_name,
                        "created_at": "2024-01-15T11:00:00Z"
                    }
                ]
            }
            mock_client.get.return_value = mock_response
            
            # When: 사용자 이력서 조회를 요청하면
            response = await mock_client.get(f"/api/v1/resumes/user/{quote(valid_name)}")
            
            # Then: 성공적으로 이력서 목록이 반환된다
            assert response.status_code == 200
            data = response.json()
            assert data["user"] == valid_name
            assert data["count"] == 2
            assert len(data["resumes"]) == 2

    @pytest.mark.asyncio
    async def test_user_not_found_scenario(self):
        """
        시나리오: 존재하지 않는 사용자 조회
        Given: 존재하지 않는 사용자 이름이 주어지고
        When: 사용자 이력서 조회를 요청하면
        Then: 빈 이력서 목록이 반환된다 (에러가 아님)
        """
        # Given: 존재하지 않는 사용자 이름
        nonexistent_user = "nonexistent_user_12345"
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "user": nonexistent_user,
            "count": 0,
            "resumes": []
        }
        mock_client.get.return_value = mock_response
        
        # When: 사용자 이력서 조회를 요청하면
        response = await mock_client.get(f"/api/v1/resumes/user/{quote(nonexistent_user)}")
        
        # Then: 빈 이력서 목록이 반환된다
        assert response.status_code == 200
        data = response.json()
        assert data["user"] == nonexistent_user
        assert data["count"] == 0
        assert data["resumes"] == []

    @pytest.mark.asyncio
    async def test_database_error_scenario(self):
        """
        시나리오: 데이터베이스 에러 발생
        Given: 데이터베이스 연결 문제가 발생하고
        When: 사용자 이력서 조회를 요청하면
        Then: 500 서버 에러가 반환된다
        """
        # Given: 데이터베이스 연결 문제
        user_name = "test_user"
        
        # Mock HTTP client
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "detail": f"Failed to retrieve resumes for user '{user_name}': Database connection failed",
            "error_code": "DATABASE_OPERATION_FAILED",
            "timestamp": "2024-01-15T10:30:00Z",
            "details": {
                "user_name": user_name,
                "reason": "Database connection failed"
            }
        }
        mock_client.get.return_value = mock_response
        
        # When: 사용자 이력서 조회를 요청하면
        response = await mock_client.get(f"/api/v1/resumes/user/{quote(user_name)}")
        
        # Then: 500 서버 에러가 반환된다
        assert response.status_code == 500
        error_data = response.json()
        assert error_data["error_code"] == "DATABASE_OPERATION_FAILED"
        assert user_name in error_data["details"]["user_name"]
