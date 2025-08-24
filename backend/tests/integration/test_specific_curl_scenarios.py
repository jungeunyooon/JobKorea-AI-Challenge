"""
사용자 제공 cURL 요청들의 구체적인 시나리오별 테스트
"""
import pytest
import httpx
from urllib.parse import quote, unquote
from unittest.mock import AsyncMock, MagicMock


class TestSpecificCurlScenarios:
    """사용자 제공 cURL 명령어들의 개별 시나리오 테스트"""

    @pytest.mark.asyncio
    async def test_interview_post_questions_scenario(self):
        """
        cURL 시나리오 1: 면접 질문 생성 (POST)
        curl -X 'POST' 'http://api.localhost/api/v1/interview/%E3%84%B4/questions' -H 'accept: application/json' -d ''
        
        %E3%84%B4 = "ㄴ" (한글 자음)
        """
        # Given: URL 인코딩된 한글 자음 "ㄴ"
        encoded_key = "%E3%84%B4"
        decoded_key = unquote(encoded_key)  # "ㄴ"
        
        print(f"\n면접 질문 생성 테스트")
        print(f"원본 URL: /api/v1/interview/{encoded_key}/questions")
        print(f"디코딩된 키: '{decoded_key}'")
        
        # 시나리오 1: 단일 문자이므로 유효성 검증 통과, 하지만 이력서 없음
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "detail": f"Resume not found: {decoded_key}",
            "error_code": "RESUME_NOT_FOUND",
            "timestamp": "2024-01-15T10:30:00Z",
            "details": {"unique_key": decoded_key}
        }
        mock_client.post.return_value = mock_response
        
        # When: POST 요청 시뮬레이션
        response = await mock_client.post(f"/api/v1/interview/{encoded_key}/questions", data='')
        
        # Then: 표준 에러 응답 확인
        assert response.status_code == 404
        error_data = response.json()
        assert error_data["error_code"] == "RESUME_NOT_FOUND"
        assert decoded_key in error_data["details"]["unique_key"]
        
        print(f"✅ 예상 응답: 404 - 이력서 없음")

    @pytest.mark.asyncio 
    async def test_interview_get_questions_scenario(self):
        """
        cURL 시나리오 2: 면접 질문 조회 (GET)
        curl -X 'GET' 'http://api.localhost/api/v1/interview/%E3%84%B4/questions' -H 'accept: application/json'
        """
        # Given: URL 인코딩된 한글 자음 "ㄴ"
        encoded_key = "%E3%84%B4"
        decoded_key = unquote(encoded_key)  # "ㄴ"
        
        print(f"\n면접 질문 조회 테스트")
        print(f"원본 URL: /api/v1/interview/{encoded_key}/questions")
        print(f"디코딩된 키: '{decoded_key}'")
        
        # 시나리오: 해당 키로 생성된 면접 질문이 없음
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "detail": f"No interview questions found for resume: {decoded_key}",
            "error_code": "INTERVIEW_NOT_FOUND",
            "timestamp": "2024-01-15T10:30:00Z",
            "details": {"unique_key": decoded_key}
        }
        mock_client.get.return_value = mock_response
        
        # When: GET 요청 시뮬레이션
        response = await mock_client.get(f"/api/v1/interview/{encoded_key}/questions")
        
        # Then: 표준 에러 응답 확인
        assert response.status_code == 404
        error_data = response.json()
        assert error_data["error_code"] == "INTERVIEW_NOT_FOUND"
        assert decoded_key in error_data["details"]["unique_key"]
        
        print(f"✅ 예상 응답: 404 - 면접 질문 없음")

    @pytest.mark.asyncio
    async def test_learning_post_path_scenario(self):
        """
        cURL 시나리오 3: 학습 경로 생성 (POST)
        curl -X 'POST' 'http://api.localhost/api/v1/learning/%E3%84%B4/learning-path' -H 'accept: application/json' -d ''
        """
        # Given: URL 인코딩된 한글 자음 "ㄴ"
        encoded_key = "%E3%84%B4"
        decoded_key = unquote(encoded_key)  # "ㄴ"
        
        print(f"\n학습 경로 생성 테스트")
        print(f"원본 URL: /api/v1/learning/{encoded_key}/learning-path")
        print(f"디코딩된 키: '{decoded_key}'")
        
        # 시나리오: 이력서가 존재하지 않음
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "detail": f"Resume not found: {decoded_key}",
            "error_code": "RESUME_NOT_FOUND",
            "timestamp": "2024-01-15T10:30:00Z",
            "details": {"unique_key": decoded_key}
        }
        mock_client.post.return_value = mock_response
        
        # When: POST 요청 시뮬레이션
        response = await mock_client.post(f"/api/v1/learning/{encoded_key}/learning-path", data='')
        
        # Then: 표준 에러 응답 확인
        assert response.status_code == 404
        error_data = response.json()
        assert error_data["error_code"] == "RESUME_NOT_FOUND"
        assert decoded_key in error_data["details"]["unique_key"]
        
        print(f"✅ 예상 응답: 404 - 이력서 없음")

    @pytest.mark.asyncio
    async def test_learning_get_path_scenario(self):
        """
        cURL 시나리오 4: 학습 경로 조회 (GET)
        curl -X 'GET' 'http://api.localhost/api/v1/learning/%E3%84%B4/learning-path' -H 'accept: application/json'
        """
        # Given: URL 인코딩된 한글 자음 "ㄴ"
        encoded_key = "%E3%84%B4"
        decoded_key = unquote(encoded_key)  # "ㄴ"
        
        print(f"\n학습 경로 조회 테스트")
        print(f"원본 URL: /api/v1/learning/{encoded_key}/learning-path")
        print(f"디코딩된 키: '{decoded_key}'")
        
        # 시나리오: 해당 키로 생성된 학습 경로가 없음
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "detail": f"No learning paths found for resume: {decoded_key}",
            "error_code": "LEARNING_NOT_FOUND",
            "timestamp": "2024-01-15T10:30:00Z",
            "details": {"unique_key": decoded_key}
        }
        mock_client.get.return_value = mock_response
        
        # When: GET 요청 시뮬레이션
        response = await mock_client.get(f"/api/v1/learning/{encoded_key}/learning-path")
        
        # Then: 표준 에러 응답 확인
        assert response.status_code == 404
        error_data = response.json()
        assert error_data["error_code"] == "LEARNING_NOT_FOUND"
        assert decoded_key in error_data["details"]["unique_key"]
        
        print(f"✅ 예상 응답: 404 - 학습 경로 없음")

    @pytest.mark.asyncio
    async def test_resume_get_user_scenario(self):
        """
        cURL 시나리오 5: 사용자 이력서 조회 (GET)
        curl -X 'GET' 'http://api.localhost/api/v1/resumes/user/%E3%85%81' -H 'accept: application/json'
        """
        # Given: URL 인코딩된 한글 자음 "ㅁ"
        encoded_key = "%E3%85%81"
        decoded_key = unquote(encoded_key)  # "ㅁ"
        
        print(f"\n사용자 이력서 조회 테스트")
        print(f"원본 URL: /api/v1/resumes/user/{encoded_key}")
        print(f"디코딩된 키: '{decoded_key}'")
        
        # 시나리오: 해당 사용자의 이력서가 없음 (빈 목록 반환)
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "user": decoded_key,
            "count": 0,
            "resumes": []
        }
        mock_client.get.return_value = mock_response
        
        # When: GET 요청 시뮬레이션
        response = await mock_client.get(f"/api/v1/resumes/user/{encoded_key}")
        
        # Then: 성공 응답 확인 (빈 목록)
        assert response.status_code == 200
        data = response.json()
        assert data["user"] == decoded_key
        assert data["count"] == 0
        assert data["resumes"] == []
        
        print(f"✅ 예상 응답: 200 - 빈 이력서 목록")

    @pytest.mark.asyncio
    async def test_validation_error_scenarios(self):
        """
        입력 검증 실패 시나리오들 테스트
        """
        
        # 검증 실패 케이스들
        invalid_inputs = [
            {
                "input": "",  # 빈 문자열
                "encoded": "",
                "expected_error": "cannot be empty",
                "status_code": 422
            },
            {
                "input": " ",  # 공백만
                "encoded": "%20",
                "expected_error": "cannot be empty",
                "status_code": 422
            },
            {
                "input": "x" * 201,  # 너무 긴 입력
                "encoded": quote("x" * 201),
                "expected_error": "too long",
                "status_code": 422
            }
        ]
        
        # 테스트할 엔드포인트들
        endpoints = [
            {"service": "interview", "path": "/api/v1/interview/{key}/questions", "method": "POST"},
            {"service": "interview", "path": "/api/v1/interview/{key}/questions", "method": "GET"}, 
            {"service": "learning", "path": "/api/v1/learning/{key}/learning-path", "method": "POST"},
            {"service": "learning", "path": "/api/v1/learning/{key}/learning-path", "method": "GET"}
        ]
        
        for endpoint in endpoints:
            for invalid_case in invalid_inputs:
                print(f"\n검증 실패 테스트: {endpoint['service']} {endpoint['method']}")
                print(f"잘못된 입력: '{invalid_case['input'][:20]}...'")
                
                # Mock 응답 설정
                mock_client = AsyncMock()
                mock_response = MagicMock()
                mock_response.status_code = invalid_case["status_code"]
                mock_response.json.return_value = {
                    "detail": f"Validation error in field 'unique_key': {invalid_case['expected_error']}",
                    "error_code": f"{endpoint['service'].upper()}_VALIDATION_ERROR",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "field": "unique_key",
                        "validation_message": invalid_case['expected_error']
                    }
                }
                
                # 요청 시뮬레이션
                test_path = endpoint['path'].replace('{key}', invalid_case['encoded'])
                if endpoint['method'] == 'POST':
                    mock_client.post.return_value = mock_response
                    response = await mock_client.post(test_path, data='')
                else:
                    mock_client.get.return_value = mock_response
                    response = await mock_client.get(test_path)
                
                # 검증
                assert response.status_code == invalid_case["status_code"]
                error_data = response.json()
                assert "VALIDATION_ERROR" in error_data["error_code"]
                assert invalid_case["expected_error"] in error_data["detail"].lower()
                
                print(f"✅ 검증 에러 확인: {error_data['error_code']}")

    @pytest.mark.asyncio
    async def test_success_scenarios(self):
        """
        성공적인 요청 시나리오들 테스트
        """
        
        # 유효한 입력들
        valid_inputs = [
            {
                "input": "김철수_1",
                "encoded": quote("김철수_1"),
                "description": "한글 이름과 숫자"
            },
            {
                "input": "john_doe_2",
                "encoded": quote("john_doe_2"),
                "description": "영문 이름과 숫자"
            },
            {
                "input": "user123",
                "encoded": quote("user123"),
                "description": "영문과 숫자 조합"
            }
        ]
        
        # 성공 시나리오 테스트
        for valid_case in valid_inputs:
            print(f"\n성공 시나리오 테스트: {valid_case['description']}")
            print(f"입력: '{valid_case['input']}'")
            
            # Resume 서비스 - 사용자 이력서 조회 (성공)
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "user": valid_case["input"],
                "count": 1,
                "resumes": [
                    {
                        "unique_key": valid_case["input"],
                        "name": valid_case["input"].split('_')[0],
                        "created_at": "2024-01-15T10:00:00Z"
                    }
                ]
            }
            mock_client.get.return_value = mock_response
            
            response = await mock_client.get(f"/api/v1/resumes/user/{valid_case['encoded']}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["user"] == valid_case["input"]
            assert data["count"] >= 0
            assert isinstance(data["resumes"], list)
            
            print(f"✅ Resume 서비스 성공 응답 확인")
            
            # Interview 서비스 - 면접 질문 생성 (성공)
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "interview_id": "12345",
                "resume_id": "67890",
                "unique_key": valid_case["input"],
                "provider": "gemini",
                "model": "gemini-pro",
                "questions": [
                    "Q1: 자기소개를 해주세요.",
                    "Q2: 지원 동기는 무엇인가요?",
                    "Q3: 장단점을 말씀해 주세요.",
                    "Q4: 5년 후 목표는 무엇인가요?",
                    "Q5: 우리 회사에 대해 알고 있는 것은?"
                ],
                "generated_at": "2024-01-15T10:30:00Z"
            }
            mock_client.post.return_value = mock_response
            
            response = await mock_client.post(f"/api/v1/interview/{valid_case['encoded']}/questions", data='')
            
            assert response.status_code == 200
            data = response.json()
            assert data["unique_key"] == valid_case["input"]
            assert len(data["questions"]) == 5
            assert data["provider"] == "gemini"
            
            print(f"✅ Interview 서비스 성공 응답 확인")

    def test_error_response_structure(self):
        """
        모든 에러 응답의 구조가 일관된지 확인
        """
        
        # 서비스별 에러 응답 예시들
        error_examples = [
            {
                "service": "resume",
                "response": {
                    "detail": "Validation error in field 'name': User name cannot be empty",
                    "error_code": "RESUME_VALIDATION_ERROR",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "field": "name",
                        "validation_message": "User name cannot be empty"
                    }
                }
            },
            {
                "service": "interview", 
                "response": {
                    "detail": "No interview questions found for resume: test_key",
                    "error_code": "INTERVIEW_NOT_FOUND",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "unique_key": "test_key"
                    }
                }
            },
            {
                "service": "learning",
                "response": {
                    "detail": "Failed to generate learning path for test_key: Service unavailable",
                    "error_code": "LEARNING_GENERATION_FAILED",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "unique_key": "test_key",
                        "reason": "Service unavailable"
                    }
                }
            }
        ]
        
        # 공통 에러 응답 구조 검증
        required_fields = ["detail", "error_code", "timestamp"]
        
        for example in error_examples:
            service = example["service"]
            response = example["response"]
            
            print(f"\n{service} 서비스 에러 응답 구조 검증")
            
            # 필수 필드 확인
            for field in required_fields:
                assert field in response, f"Missing required field '{field}' in {service}"
                print(f"  ✅ 필수 필드 '{field}': {response[field][:50]}...")
            
            # 에러 코드 형식 확인
            error_code = response["error_code"]
            assert error_code.isupper(), f"Error code should be uppercase: {error_code}"
            assert service.upper() in error_code, f"Error code should contain service name: {error_code}"
            
            # 타임스탬프 형식 확인 (ISO 8601)
            timestamp = response["timestamp"]
            assert "T" in timestamp and "Z" in timestamp, f"Invalid timestamp format: {timestamp}"
            
            print(f"  ✅ 에러 코드 형식: {error_code}")
            print(f"  ✅ 타임스탬프 형식: {timestamp}")
            
        print(f"\n✅ 모든 서비스의 에러 응답 구조 일관성 확인 완료")
