# AI Challenge 프로젝트 가이드라인

## 프로젝트 개요
- **목표**: 구직자 이력서 기반 맞춤형 면접 질문 생성 및 학습 경로 추천
- **아키텍처**: MSA (Microservices Architecture) 
- **핵심 기술**: FastAPI, MongoDB, Docker, Traefik, LLM APIs

## 서비스 구조

### 1. Resume Service (이력서 관리)
```python
# 책임: 이력서 CRUD, 데이터 검증, 스키마 관리
# 엔드포인트: /api/v1/resumes/
# 핵심 기능: 생성, 조회, 수정, 삭제
```

### 2. Interview Service (면접 질문 생성)  
```python
# 책임: AI 기반 면접 질문 생성, LLM 통합
# 엔드포인트: /api/v1/interview/{unique_key}/questions
# 핵심 기능: 5개 다차원 질문 생성, 난이도 분배
```

### 3. Learning Service (학습 경로 추천)
```python
# 책임: 개인 맞춤형 학습 경로 생성, 강점/약점 분석
# 엔드포인트: /api/v1/learning/{unique_key}/learning-path  
# 핵심 기능: 장점 심화, 약점 보완 학습 경로 5개 생성
```

### 4. Shared Module (공통 모듈)
```python
# 구성요소:
# - llm/: LLM 클라이언트 (OpenAI, Claude, Gemini)
# - utils/: JSON 파서, 이력서 포맷터, 예외 처리
# - config/: 설정 관리
# - database/: MongoDB 연결 및 컬렉션 관리
```

## 코딩 스타일

### 네이밍 컨벤션
```python
# 함수: 동사_명사 (snake_case)
async def generate_interview_questions()
async def validate_resume_data()
async def parse_llm_response()

# 변수: 명확한 의미 표현
resume_data: dict       # Good
data: dict             # Avoid
unique_key: str        # Good  
key: str               # Avoid

# 상수: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_QUESTION_COUNT = 5
LLM_TIMEOUT_SECONDS = 30
```

### 파일 구조 표준
```
service-name/
├── main.py              # FastAPI 앱 엔트리포인트
├── config.py            # 서비스별 설정
├── database.py          # DB 연결 설정
├── logger.py            # 로깅 설정
├── requirements.txt     # 의존성
├── Dockerfile          # 컨테이너 설정
├── prompts/            # LLM 프롬프트 (YAML)
└── src/
    ├── __init__.py
    ├── routes.py       # API 라우터
    ├── schemas.py      # Pydantic 모델
    ├── service.py      # 비즈니스 로직
    └── crud.py         # 데이터 접근 (필요시)
```

## LLM 통합 패턴

### 1. 프롬프트 관리
```yaml
# prompts/*.yaml 형식
name: "question_generation"
version: "3.0.0"
system_prompt_template: |
  당신은 백엔드 개발자 채용 전문 기술 면접관입니다...
  
human_prompt_template: |
  지원자 정보: {name}
  프로젝트 경험: {projects}
  
output_schema:
  questions:
    - difficulty: string
      topic: string  
      question: string
```

### 2. LLM 클라이언트 사용
```python
# shared.llm.registry 활용
from shared.llm.registry import get_llm_client

async def generate_content(prompt: str, provider: str = "gemini") -> str:
    client = get_llm_client(provider)
    response = await client.ainvoke([HumanMessage(content=prompt)])
    return response.content
```

### 3. 응답 파싱 패턴
```python
# shared.utils.json_parser 활용
from shared.utils.json_parser import parse_llm_json_response

try:
    parsed = parse_llm_json_response(
        response_text,
        expected_keys=["questions", "summary"],
        fallback_keys={"questions": ["items", "q_list"]}
    )
    return parsed["questions"]
except JSONDecodeError:
    # 폴백 로직 또는 재시도
```

## 에러 처리 가이드

### 1. 계층별 에러 처리
```python
# 1단계: 비즈니스 로직 에러 (service.py)
class ResumeNotFoundError(Exception):
    pass

class LLMServiceError(Exception):
    pass

# 2단계: HTTP 에러 변환 (routes.py)  
@router.post("/{unique_key}/questions")
async def generate_questions(unique_key: str):
    try:
        result = await interview_service.generate(unique_key)
        return result
    except ResumeNotFoundError:
        raise HTTPException(status_code=404, detail="Resume not found")
    except LLMServiceError:
        raise HTTPException(status_code=503, detail="AI service unavailable")
```

### 2. 로깅 패턴
```python
import logging
logger = logging.getLogger(__name__)

# 에러 로깅
try:
    result = await llm_client.generate(prompt)
except Exception as e:
    logger.error(
        "LLM generation failed",
        extra={
            "unique_key": unique_key,
            "provider": provider,
            "error": str(e),
            "prompt_length": len(prompt)
        }
    )
    raise
```

## 테스트 전략

### 1. 테스트 구조
```python
# Given-When-Then 패턴
@pytest.mark.asyncio
async def test_generate_interview_questions():
    # Given: 유효한 이력서가 주어지고
    unique_key = "test_user_1"
    
    # When: 면접 질문 생성을 요청하면
    response = await client.post(f"/interview/{unique_key}/questions")
    
    # Then: 5개의 질문이 생성된다
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 5
```

### 2. Mock 활용
```python
# LLM API 모킹
@pytest.fixture
def mock_llm_response():
    return {
        "questions": [
            {"question": "테스트 질문", "difficulty": "medium"}
        ]
    }

@patch('shared.llm.registry.get_llm_client')
async def test_with_mock_llm(mock_client, mock_llm_response):
    mock_client.return_value.ainvoke.return_value.content = json.dumps(mock_llm_response)
    # 테스트 로직...
```

## 배포 및 운영

### 1. Docker 설정
```dockerfile
# 각 서비스별 Dockerfile 표준
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. 환경 변수 관리
```python
# config.py 표준 패턴
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    mongodb_url: str = Field(..., env="MONGODB_URL")
    
    # LLM APIs
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    claude_api_key: str = Field(..., env="CLAUDE_API_KEY")
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    
    # Service
    service_name: str = Field("interview-service", env="SERVICE_NAME")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
```

## 성능 최적화

### 1. 비동기 패턴
```python
# 모든 I/O 작업은 async/await
async def process_multiple_resumes(resume_keys: List[str]) -> List[dict]:
    tasks = [process_single_resume(key) for key in resume_keys]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if not isinstance(r, Exception)]
```

### 2. 캐싱 전략
```python
# 자주 요청되는 데이터 캐싱 고려
from functools import lru_cache

@lru_cache(maxsize=100)
def get_formatted_resume(resume_data: str) -> str:
    # 이력서 포맷팅 결과 캐싱
    return format_resume_for_llm(json.loads(resume_data))
```

이 가이드라인을 따라 일관성 있는 고품질 코드를 작성해주세요!
