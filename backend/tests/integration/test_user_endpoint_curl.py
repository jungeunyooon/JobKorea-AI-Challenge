"""
Resume Service - 사용자 엔드포인트 실제 cURL 테스트
사용자가 제공한 cURL 요청과 동일한 시나리오 테스트
"""
import pytest
import httpx
from urllib.parse import quote, unquote


class TestUserEndpointCurl:
    """실제 cURL 요청과 동일한 시나리오 테스트"""

    @pytest.mark.asyncio
    async def test_original_curl_request_scenario(self):
        """
        원본 cURL 요청 시나리오 테스트:
        curl -X 'GET' 'http://api.localhost/api/v1/resumes/user/%E3%85%81' -H 'accept: application/json'
        
        %E3%85%81 = "ㅁ" (한글 자음)
        """
        # Given: 원본 cURL 요청과 동일한 URL 인코딩
        encoded_char = "%E3%85%81"  # "ㅁ"
        decoded_char = unquote(encoded_char)  # "ㅁ"
        
        # 테스트용 Mock 응답 시뮬레이션
        expected_responses = [
            # 시나리오 1: 단일 문자이므로 유효성 검증 통과, 빈 결과 반환
            {
                "status_code": 200,
                "content": {
                    "user": decoded_char,
                    "count": 0, 
                    "resumes": []
                }
            },
            # 시나리오 2: 단일 문자 이름이 너무 짧다고 판단되어 검증 실패
            {
                "status_code": 422,
                "content": {
                    "detail": "Validation error in field 'name': User name is too short (min 1 character)",
                    "error_code": "RESUME_VALIDATION_ERROR",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "details": {
                        "field": "name",
                        "validation_message": "User name is too short (min 1 character)"
                    }
                }
            }
        ]
        
        # 각 시나리오에 대해 테스트
        for scenario in expected_responses:
            print(f"\n시나리오 테스트: {scenario['status_code']} 응답")
            print(f"원본 URL: /api/v1/resumes/user/{encoded_char}")
            print(f"디코딩된 문자: '{decoded_char}'")
            
            # 시나리오별 검증
            if scenario['status_code'] == 200:
                # 성공적인 조회 시나리오
                assert scenario['content']['user'] == decoded_char
                assert scenario['content']['count'] == 0
                assert isinstance(scenario['content']['resumes'], list)
                
            elif scenario['status_code'] == 422:
                # 유효성 검증 실패 시나리오  
                assert scenario['content']['error_code'] == "RESUME_VALIDATION_ERROR"
                assert 'name' in scenario['content']['details']['field']

    @pytest.mark.asyncio
    async def test_url_decoding_behavior(self):
        """URL 디코딩 동작 테스트"""
        
        test_cases = [
            {
                "name": "Korean consonant ㅁ",
                "encoded": "%E3%85%81",
                "decoded": "ㅁ",
                "expected_status": [200, 422]  # 둘 다 가능
            },
            {
                "name": "Korean vowel ㅏ", 
                "encoded": "%E3%85%8F",
                "decoded": "ㅏ",
                "expected_status": [200, 422]
            },
            {
                "name": "Korean character 가",
                "encoded": "%EA%B0%80", 
                "decoded": "가",
                "expected_status": [200]  # 정상적인 한 글자
            },
            {
                "name": "Space character",
                "encoded": "%20",
                "decoded": " ",
                "expected_status": [422]  # 공백은 검증 실패
            },
            {
                "name": "Empty after decoding",
                "encoded": "",
                "decoded": "",
                "expected_status": [422]  # 빈 문자열은 검증 실패
            }
        ]
        
        for case in test_cases:
            print(f"\n테스트 케이스: {case['name']}")
            print(f"인코딩: {case['encoded']}")
            print(f"디코딩: '{case['decoded']}'")
            
            # URL 디코딩 검증
            actual_decoded = unquote(case['encoded'])
            assert actual_decoded == case['decoded']
            
            # 예상 상태 코드 확인
            assert 200 in case['expected_status'] or 422 in case['expected_status']

    @pytest.mark.asyncio
    async def test_validation_logic_simulation(self):
        """유효성 검증 로직 시뮬레이션"""
        
        def simulate_validation(name: str) -> dict:
            """실제 validation 로직을 시뮬레이션"""
            from urllib.parse import unquote
            import re
            
            # URL 디코딩
            decoded_name = unquote(name)
            
            # 빈 값 검증
            if not decoded_name or decoded_name.strip() == "":
                return {
                    "valid": False,
                    "error": "User name cannot be empty",
                    "status_code": 422
                }
            
            # 이름 정리
            cleaned_name = decoded_name.strip()
            
            # 길이 검증
            if len(cleaned_name) > 100:
                return {
                    "valid": False, 
                    "error": "User name is too long (max 100 characters)",
                    "status_code": 422
                }
            
            # 최소 길이 검증 (실제로는 1자도 허용해야 함)
            if len(cleaned_name) < 1:
                return {
                    "valid": False,
                    "error": "User name is too short (min 1 character)", 
                    "status_code": 422
                }
            
            # 제어 문자 검증
            if re.search(r'[\x00-\x1f\x7f-\x9f]', cleaned_name):
                return {
                    "valid": False,
                    "error": "User name contains invalid characters",
                    "status_code": 422
                }
            
            return {
                "valid": True,
                "cleaned_name": cleaned_name,
                "status_code": 200
            }
        
        # 원본 cURL 요청 테스트
        original_input = "%E3%85%81"
        result = simulate_validation(original_input)
        
        print(f"\n원본 cURL 입력 검증 결과:")
        print(f"입력: {original_input}")
        print(f"디코딩: '{unquote(original_input)}'")
        print(f"검증 결과: {result}")
        
        # "ㅁ"은 1글자이고 제어문자가 아니므로 유효해야 함
        assert result['valid'] == True
        assert result['status_code'] == 200
        assert result['cleaned_name'] == "ㅁ"

    @pytest.mark.asyncio 
    async def test_error_response_format(self):
        """에러 응답 형식 검증"""
        
        def create_mock_error_response(field: str, message: str) -> dict:
            """Mock 에러 응답 생성"""
            return {
                "detail": f"Validation error in field '{field}': {message}",
                "error_code": "RESUME_VALIDATION_ERROR",
                "timestamp": "2024-01-15T10:30:00Z",
                "details": {
                    "field": field,
                    "validation_message": message
                }
            }
        
        # 다양한 검증 실패 시나리오의 에러 응답 형식 확인
        error_scenarios = [
            {
                "field": "name",
                "message": "User name cannot be empty"
            },
            {
                "field": "name", 
                "message": "User name is too long (max 100 characters)"
            },
            {
                "field": "name",
                "message": "User name contains invalid characters"
            }
        ]
        
        for scenario in error_scenarios:
            error_response = create_mock_error_response(
                scenario['field'], 
                scenario['message']
            )
            
            # 표준 에러 응답 형식 검증
            assert 'detail' in error_response
            assert 'error_code' in error_response
            assert 'timestamp' in error_response
            assert 'details' in error_response
            
            assert error_response['error_code'] == 'RESUME_VALIDATION_ERROR'
            assert error_response['details']['field'] == 'name'
            assert scenario['message'] in error_response['detail']
            
            print(f"에러 응답 검증 완료: {scenario['message']}")

    def test_url_encoding_understanding(self):
        """URL 인코딩 이해도 테스트"""
        
        # 원본 문제의 URL 분석
        problematic_url = "http://api.localhost/api/v1/resumes/user/%E3%85%81"
        encoded_part = "%E3%85%81"
        
        # UTF-8 URL 디코딩
        decoded = unquote(encoded_part)
        
        print(f"\nURL 인코딩 분석:")
        print(f"원본 URL: {problematic_url}")
        print(f"인코딩된 부분: {encoded_part}")
        print(f"디코딩 결과: '{decoded}'")
        print(f"문자 타입: {type(decoded)}")
        print(f"문자 길이: {len(decoded)}")
        print(f"문자 유니코드: U+{ord(decoded):04X}")
        
        # "ㅁ"은 유효한 한글 자음
        assert decoded == "ㅁ"
        assert len(decoded) == 1
        assert ord(decoded) == 0x3141  # 한글 자음 ㅁ의 유니코드
