# GitHub Copilot 가이드라인

> AI Challenge - Interview Preparation API 프로젝트의 GitHub Copilot 활용 가이드

## 🎯 프로젝트 컨텍스트

### 핵심 아키텍처
- **MSA 구조**: resume-service, interview-service, learning-service
- **기술 스택**: FastAPI + MongoDB + Docker + Traefik
- **LLM 통합**: OpenAI, Claude, Gemini 멀티 프로바이더

### 도메인 이해
```python
# 이력서 → 면접 질문 생성 플로우
resume_data → format_for_llm() → generate_questions() → parse_response()

# 이력서 → 학습 경로 추천 플로우  
resume_data → analyze_strengths_weaknesses() → recommend_paths() → parse_response()
```

## ⚡ Copilot 활용 전략

### 1. 코드 생성 시 우선순위

#### ✅ 권장 패턴
```python
# 함수형 + 타입 힌트 + 조기 반환
async def validate_resume_data(resume_data: dict) -> dict:
    if not resume_data:
        raise ValueError("Resume data is required")
    
    if not resume_data.get("name"):
        raise ValueError("Name is required")
    
    # 메인 로직
    return validated_data
```

#### ❌ 피해야 할 패턴
```python
# 클래스 지향, 깊은 중첩
class ResumeProcessor:
    def process(self, data):
        if data:
            if data.get("name"):
                # 깊은 중첩...
```

### 2. FastAPI 라우터 생성

#### Copilot 프롬프트 예시:
```python
# FastAPI 라우터 생성 요청 시
# "Create FastAPI POST endpoint for interview questions generation with:
# - Path: /interview/{unique_key}/questions  
# - Response model: InterviewQuestionsResponse
# - Error handling: 404 for invalid resume, 500 for LLM errors
# - Provider parameter support"

@router.post("/{unique_key}/questions", response_model=InterviewQuestionsResponse)
async def generate_interview_questions(
    unique_key: str,
    provider: str = "gemini",
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> InterviewQuestionsResponse:
    # Copilot이 생성할 내용...
```

### 3. LLM 통합 코드

#### 프롬프트 힌트:
```python
# "Create LLM service function with fallback strategy:
# - Primary: Gemini, Fallback: OpenAI → Claude
# - JSON response parsing with retry logic
# - Error handling for rate limits and parsing failures"

async def call_llm_with_fallback(
    messages: List[BaseMessage],
    providers: List[str] = ["gemini", "openai", "claude"]
) -> Dict[str, Any]:
    # Copilot 생성 영역...
```

### 4. 테스트 코드 생성

#### BDD 패턴 요청:
```python
# "Generate pytest BDD test for interview service:
# - Given: Valid resume exists
# - When: POST /interview/{key}/questions
# - Then: 5 questions returned with proper structure"

@pytest.mark.asyncio
async def test_generate_interview_questions_success(http_client):
    # Given: ...
    # When: ...  
    # Then: ...
```

## 🛠 코딩 컨벤션

### 네이밍 규칙
```python
# 함수: 동사_명사 형태
async def generate_interview_questions()
async def validate_resume_data()
async def parse_llm_response()

# 변수: 명확한 의미
resume_data (O) vs data (X)
question_list (O) vs items (X)
llm_provider (O) vs provider (X)
```

### 에러 처리 패턴
```python
# Copilot에게 요청할 패턴
try:
    result = await llm_service.generate(prompt)
    return parse_response(result)
except LLMApiError as e:
    logger.error(f"LLM API failed: {e}")
    raise HTTPException(status_code=503, detail="AI service unavailable")
except JSONDecodeError as e:
    logger.error(f"Failed to parse LLM response: {e}")
    raise HTTPException(status_code=500, detail="Invalid AI response format")
```

### MongoDB 쿼리 패턴
```python
# Copilot 요청: "MongoDB query with error handling"
async def get_resume_by_key(db: AsyncIOMotorDatabase, unique_key: str) -> dict:
    try:
        resume = await db.resumes.find_one({"unique_key": unique_key})
        if not resume:
            raise ResumeNotFoundError(f"Resume {unique_key} not found")
        return resume
    except PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise DatabaseError("Failed to retrieve resume")
```

## 🔧 유틸리티 생성 가이드

### JSON 파싱 유틸리티
```python
# Copilot 프롬프트: "Create robust JSON parser for LLM responses:
# - Remove markdown blocks
# - Handle partial JSON
# - Fallback key mapping
# - Retry mechanism"
```

### 이력서 포맷터
```python
# Copilot 프롬프트: "Format resume data for LLM prompt:
# - Extract project details
# - Highlight tech stack
# - Include experience duration
# - Remove sensitive info"
```

## 📋 TODO 주석 활용

### Copilot 가이드용 주석
```python
# TODO: Generate FastAPI endpoint for learning path
# TODO: Add rate limiting for LLM API calls  
# TODO: Implement caching for frequently requested resumes
# TODO: Add monitoring metrics for API response times

# FIXME: Handle edge case when LLM returns empty response
# NOTE: This function assumes resume data is pre-validated
# HACK: Temporary workaround for Gemini API quirks
```

## 🚀 고급 활용 팁

### 1. 컨텍스트 제공
```python
# 파일 상단에 컨텍스트 주석
"""
Interview Service - AI 기반 면접 질문 생성
- 입력: 이력서 unique_key  
- 처리: LLM 프롬프트 → JSON 응답 파싱
- 출력: 5개 구조화된 면접 질문
- 의존성: shared.llm.registry, shared.utils.json_parser
"""
```

### 2. 단계별 구현 요청
```python
# Step 1: 데이터 검증
# Step 2: LLM 프롬프트 생성  
# Step 3: API 호출
# Step 4: 응답 파싱
# Step 5: 에러 핸들링
```

### 3. 성능 최적화 힌트
```python
# "Optimize this function for:
# - Async/await best practices
# - Memory efficiency for large resume data
# - Caching frequently used LLM responses
# - Connection pooling for database"
```

## ⚠️ 주의사항

### 생성 금지 패턴
- ❌ 하드코딩된 API 키나 민감 정보
- ❌ 블로킹 동기 함수 (requests 대신 httpx 사용)
- ❌ 글로벌 변수나 상태 공유
- ❌ 타입 힌트 없는 함수

### 검토 필수 영역
- 🔍 LLM API 키 사용 부분
- 🔍 데이터베이스 쿼리 최적화
- 🔍 에러 메시지의 사용자 친화성
- 🔍 로깅 레벨 및 민감 정보 마스킹

## 📚 학습 리소스

### Copilot과 함께 익혀야 할 패턴
1. **FastAPI Dependency Injection** 패턴
2. **Async/Await** 최적 활용법
3. **Pydantic 모델** 설계 원칙
4. **MongoDB ODM** 쿼리 최적화
5. **LLM 프롬프트 엔지니어링** 기법

---

> 💡 **팁**: Copilot에게 구체적이고 맥락이 있는 주석을 제공할수록 더 정확한 코드를 생성합니다!
