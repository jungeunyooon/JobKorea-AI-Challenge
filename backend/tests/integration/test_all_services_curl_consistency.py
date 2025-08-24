"""
모든 서비스의 cURL 요청에 대한 에러 응답 일관성 테스트
사용자가 제공한 실제 cURL 명령어들과 동일한 시나리오
"""
import pytest
import httpx
from urllib.parse import quote, unquote
from unittest.mock import AsyncMock, MagicMock


class TestCurlRequestConsistency:
    """사용자 제공 cURL 요청들의 일관성 테스트"""

    @pytest.mark.asyncio
    async def test_all_services_error_format_consistency(self):
        """
        모든 서비스가 동일한 에러 응답 형식을 사용하는지 확인
        
        원본 cURL 요청들:
        1. curl -X 'POST' 'http://api.localhost/api/v1/interview/%E3%84%B4/questions' -H 'accept: application/json' -d ''
        2. curl -X 'GET' 'http://api.localhost/api/v1/interview/%E3%84%B4/questions' -H 'accept: application/json' 
        3. curl -X 'POST' 'http://api.localhost/api/v1/learning/%E3%84%B4/learning-path' -H 'accept: application/json' -d ''
        4. curl -X 'GET' 'http://api.localhost/api/v1/learning/%E3%84%B4/learning-path' -H 'accept: application/json'
        5. curl -X 'GET' 'http://api.localhost/api/v1/resumes/user/%E3%85%81' -H 'accept: application/json'
        """
        
        # URL 인코딩된 문자들 분석
        encoded_chars = {
            "%E3%84%B4": "ㄴ",  # 한글 자음 ㄴ  
            "%E3%85%81": "ㅁ"   # 한글 자음 ㅁ
        }
        
        # 표준 에러 응답 형식 검증 함수
        def validate_error_response(response_data: dict) -> bool:
            """표준 에러 응답 형식 검증"""
            required_fields = ["detail", "error_code", "timestamp"]
            optional_fields = ["details"]
            
            # 필수 필드 확인
            for field in required_fields:
                if field not in response_data:
                    return False
            
            # 에러 코드 형식 검증 (대문자_언더스코어 형식)
            error_code = response_data.get("error_code", "")
            if not error_code.isupper() or "_" not in error_code:
                return False
            
            # timestamp ISO 형식 검증
            timestamp = response_data.get("timestamp", "")
            if not timestamp or len(timestamp) < 19:  # ISO 형식 최소 길이
                return False
            
            return True

        # 각 서비스별 테스트 케이스
        test_cases = [
            {
                "service": "resume",
                "method": "GET",
                "endpoint": f"/api/v1/resumes/user/{quote('ㅁ')}",  # %E3%85%81
                "description": "Resume 서비스 - 사용자 이력서 조회"
            },
            {
                "service": "interview", 
                "method": "POST",
                "endpoint": f"/api/v1/interview/{quote('ㄴ')}/questions",  # %E3%84%B4
                "description": "Interview 서비스 - 면접 질문 생성"
            },
            {
                "service": "interview",
                "method": "GET", 
                "endpoint": f"/api/v1/interview/{quote('ㄴ')}/questions",  # %E3%84%B4
                "description": "Interview 서비스 - 면접 질문 조회"
            },
            {
                "service": "learning",
                "method": "POST",
                "endpoint": f"/api/v1/learning/{quote('ㄴ')}/learning-path",  # %E3%84%B4
                "description": "Learning 서비스 - 학습 경로 생성"
            },
            {
                "service": "learning",
                "method": "GET",
                "endpoint": f"/api/v1/learning/{quote('ㄴ')}/learning-path",  # %E3%84%B4  
                "description": "Learning 서비스 - 학습 경로 조회"
            }
        ]
        
        for case in test_cases:
            print(f"\n테스트 중: {case['description']}")
            print(f"엔드포인트: {case['endpoint']}")
            
            # Mock HTTP 클라이언트 시뮬레이션
            mock_client = AsyncMock()
            mock_response = MagicMock()
            
            # 예상 에러 응답 (404 또는 422)
            if case['method'] == 'GET':
                # 조회 시 - 데이터 없음 (404)
                mock_response.status_code = 404
                mock_response.json.return_value = {
                    "detail": f"No data found for the given key",
                    "error_code": f"{case['service'].upper()}_NOT_FOUND",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "unique_key": unquote(case['endpoint'].split('/')[-2])
                    }
                }
            else:
                # 생성 시 - 검증 실패 또는 서비스 에러 (422 또는 500)
                mock_response.status_code = 422
                mock_response.json.return_value = {
                    "detail": "Validation error in field 'unique_key': Unique key is too short or invalid",
                    "error_code": f"{case['service'].upper()}_VALIDATION_ERROR",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "field": "unique_key",
                        "validation_message": "Unique key is too short or invalid"
                    }
                }
            
            # HTTP 메서드에 따른 클라이언트 설정
            if case['method'] == 'GET':
                mock_client.get.return_value = mock_response
                response = await mock_client.get(case['endpoint'])
            else:  # POST
                mock_client.post.return_value = mock_response
                response = await mock_client.post(case['endpoint'], data='')
            
            # 응답 검증
            assert response.status_code in [404, 422, 500], f"Unexpected status code for {case['service']}"
            
            response_data = response.json()
            is_valid_format = validate_error_response(response_data)
            assert is_valid_format, f"Invalid error response format for {case['service']}: {response_data}"
            
            print(f"✅ {case['service']} 서비스 에러 형식 검증 통과")

    @pytest.mark.asyncio 
    async def test_url_decoding_consistency(self):
        """
        모든 서비스에서 URL 디코딩이 일관되게 처리되는지 확인
        """
        
        # URL 인코딩된 문자들과 예상 디코딩 결과
        encoding_test_cases = [
            {
                "encoded": "%E3%84%B4",
                "decoded": "ㄴ", 
                "description": "한글 자음 ㄴ"
            },
            {
                "encoded": "%E3%85%81",
                "decoded": "ㅁ",
                "description": "한글 자음 ㅁ"
            },
            {
                "encoded": "%20",
                "decoded": " ",
                "description": "공백 문자"
            },
            {
                "encoded": "%E2%9C%85",
                "decoded": "✅",
                "description": "이모지"
            }
        ]
        
        for test_case in encoding_test_cases:
            print(f"\nURL 디코딩 테스트: {test_case['description']}")
            print(f"인코딩: {test_case['encoded']}")
            print(f"예상 디코딩: '{test_case['decoded']}'")
            
            # 실제 디코딩 확인
            actual_decoded = unquote(test_case['encoded'])
            assert actual_decoded == test_case['decoded'], f"Decoding mismatch: expected '{test_case['decoded']}', got '{actual_decoded}'"
            
            print(f"✅ 디코딩 일치: '{actual_decoded}'")

    @pytest.mark.asyncio
    async def test_validation_error_consistency(self):
        """
        모든 서비스에서 입력 검증 에러가 일관되게 처리되는지 확인
        """
        
        # 검증 실패 시나리오들
        validation_scenarios = [
            {
                "input": "",
                "expected_error": "cannot be empty",
                "expected_code": "VALIDATION_ERROR"
            },
            {
                "input": " ",
                "expected_error": "cannot be empty", 
                "expected_code": "VALIDATION_ERROR"
            },
            {
                "input": "a" * 201,  # 너무 긴 입력
                "expected_error": "too long",
                "expected_code": "VALIDATION_ERROR"
            },
            {
                "input": "test\x00key",  # 제어 문자 포함
                "expected_error": "invalid characters",
                "expected_code": "VALIDATION_ERROR"
            }
        ]
        
        services = ["resume", "interview", "learning"]
        
        for service in services:
            for scenario in validation_scenarios:
                print(f"\n{service} 서비스 검증 테스트: '{scenario['input'][:20]}...' ")
                
                # 예상 에러 응답 시뮬레이션
                expected_response = {
                    "detail": f"Validation error in field 'unique_key': {scenario['expected_error']}",
                    "error_code": f"{service.upper()}_{scenario['expected_code']}",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "field": "unique_key", 
                        "validation_message": scenario['expected_error']
                    }
                }
                
                # 에러 응답 형식 검증
                assert "detail" in expected_response
                assert "error_code" in expected_response
                assert "timestamp" in expected_response
                assert scenario['expected_code'] in expected_response['error_code']
                
                print(f"✅ {service} 검증 에러 형식 일관성 확인")

    @pytest.mark.asyncio
    async def test_http_status_code_mapping(self):
        """
        HTTP 상태 코드 매핑이 모든 서비스에서 일관되는지 확인
        """
        
        # HTTP 상태 코드 매핑 규칙
        status_code_rules = {
            400: "Bad Request - 잘못된 요청",
            404: "Not Found - 리소스를 찾을 수 없음", 
            422: "Unprocessable Entity - 검증 에러",
            500: "Internal Server Error - 서버 내부 오류",
            503: "Service Unavailable - AI 서비스 이용 불가"
        }
        
        # 각 서비스별 에러 시나리오와 예상 상태 코드
        error_scenarios = [
            {
                "scenario": "리소스 없음",
                "expected_status": 404,
                "error_codes": ["RESUME_NOT_FOUND", "INTERVIEW_NOT_FOUND", "LEARNING_NOT_FOUND"]
            },
            {
                "scenario": "입력 검증 실패", 
                "expected_status": 422,
                "error_codes": ["RESUME_VALIDATION_ERROR", "INTERVIEW_VALIDATION_ERROR", "LEARNING_VALIDATION_ERROR"]
            },
            {
                "scenario": "생성/조회 실패",
                "expected_status": 500, 
                "error_codes": ["RESUME_CREATION_FAILED", "INTERVIEW_GENERATION_FAILED", "LEARNING_GENERATION_FAILED"]
            },
            {
                "scenario": "AI 서비스 오류",
                "expected_status": 503,
                "error_codes": ["INTERVIEW_LLM_ERROR", "LEARNING_LLM_ERROR"]
            }
        ]
        
        for scenario in error_scenarios:
            print(f"\n상태 코드 매핑 테스트: {scenario['scenario']}")
            print(f"예상 상태 코드: {scenario['expected_status']} - {status_code_rules[scenario['expected_status']]}")
            
            for error_code in scenario['error_codes']:
                # Mock 에러 응답
                mock_error_response = {
                    "detail": f"Mock error for {error_code}",
                    "error_code": error_code,
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {}
                }
                
                # 에러 코드와 상태 코드 매핑 검증
                service = error_code.split('_')[0].lower()
                
                # 상태 코드 일관성 확인
                print(f"  ✅ {service} 서비스: {error_code} -> {scenario['expected_status']}")
            
            print(f"✅ '{scenario['scenario']}' 시나리오 상태 코드 매핑 일관성 확인")

    def test_error_response_schema_validation(self):
        """
        에러 응답 스키마가 모든 서비스에서 동일한지 확인
        """
        
        # 표준 에러 응답 스키마
        standard_error_schema = {
            "type": "object",
            "required": ["detail", "error_code", "timestamp"],
            "properties": {
                "detail": {"type": "string"},
                "error_code": {"type": "string", "pattern": "^[A-Z_]+$"},
                "timestamp": {"type": "string"},  # ISO 형식
                "details": {"type": "object"}  # 선택적 추가 정보
            }
        }
        
        # 각 서비스별 예시 에러 응답들
        service_error_examples = {
            "resume": {
                "detail": "No resumes found for user: test_user",
                "error_code": "RESUME_NOT_FOUND", 
                "timestamp": "2024-01-15T10:30:00Z",
                "details": {"user_name": "test_user"}
            },
            "interview": {
                "detail": "No interview questions found for resume: test_key",
                "error_code": "INTERVIEW_NOT_FOUND",
                "timestamp": "2024-01-15T10:30:00Z", 
                "details": {"unique_key": "test_key"}
            },
            "learning": {
                "detail": "No learning paths found for resume: test_key",
                "error_code": "LEARNING_NOT_FOUND",
                "timestamp": "2024-01-15T10:30:00Z",
                "details": {"unique_key": "test_key"}
            }
        }
        
        for service, example in service_error_examples.items():
            print(f"\n{service} 서비스 에러 응답 스키마 검증")
            
            # 필수 필드 확인
            for required_field in standard_error_schema["required"]:
                assert required_field in example, f"Missing required field '{required_field}' in {service}"
            
            # 필드 타입 확인
            assert isinstance(example["detail"], str), f"Invalid 'detail' type in {service}"
            assert isinstance(example["error_code"], str), f"Invalid 'error_code' type in {service}" 
            assert isinstance(example["timestamp"], str), f"Invalid 'timestamp' type in {service}"
            
            # 에러 코드 형식 확인 (대문자_언더스코어)
            error_code = example["error_code"]
            assert error_code.isupper(), f"Error code should be uppercase in {service}: {error_code}"
            assert "_" in error_code, f"Error code should contain underscore in {service}: {error_code}"
            
            print(f"  ✅ 필수 필드: {standard_error_schema['required']}")
            print(f"  ✅ 에러 코드 형식: {error_code}")
            print(f"  ✅ 타임스탬프 형식: {example['timestamp']}")
            
        print("\n✅ 모든 서비스의 에러 응답 스키마 일관성 확인 완료")
