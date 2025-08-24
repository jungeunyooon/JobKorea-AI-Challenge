# 에러 처리 가이드

> AI Challenge API의 표준화된 에러 처리 및 응답 형식

## 표준 에러 응답 형식

모든 API 에러는 다음과 같은 일관된 형식으로 응답됩니다:

```json
{
  "detail": "Resume not found with key: test_user_1",
  "error_code": "RESUME_NOT_FOUND",
  "timestamp": "2024-01-15T10:30:00Z",
  "details": {
    "unique_key": "test_user_1"
  },
  "request_id": "req_abc123def456"
}
```

### 필수 필드

- **`detail`**: 사람이 읽을 수 있는 에러 메시지
- **`error_code`**: 표준화된 에러 코드 (enum)
- **`timestamp`**: 에러 발생 시각 (ISO 8601 UTC)

### 선택적 필드

- **`details`**: 추가적인 컨텍스트 정보
- **`request_id`**: 요청 추적을 위한 고유 ID

## HTTP 상태 코드

| 상태 코드 | 설명 | 사용 시점 |
|----------|------|----------|
| `400` | Bad Request | 잘못된 요청 형식, 파라미터 오류 |
| `401` | Unauthorized | 인증 실패 |
| `403` | Forbidden | 권한 부족 |
| `404` | Not Found | 리소스를 찾을 수 없음 |
| `422` | Unprocessable Entity | 요청 데이터 유효성 검증 실패 |
| `429` | Too Many Requests | API 호출 한도 초과 |
| `500` | Internal Server Error | 서버 내부 오류 |
| `503` | Service Unavailable | 외부 서비스 이용 불가 |
| `504` | Gateway Timeout | 외부 API 호출 타임아웃 |

## 서비스별 에러 코드

### Resume Service (1000-1999)

```typescript
enum ResumeErrorCode {
  RESUME_NOT_FOUND = "RESUME_NOT_FOUND",           // 1001
  RESUME_CREATION_FAILED = "RESUME_CREATION_FAILED", // 1002
  RESUME_VALIDATION_ERROR = "RESUME_VALIDATION_ERROR", // 1003
  RESUME_UPDATE_FAILED = "RESUME_UPDATE_FAILED",   // 1004
  RESUME_DELETE_FAILED = "RESUME_DELETE_FAILED"    // 1005
}
```

**예시 응답:**
```json
{
  "detail": "Resume not found with key: john_doe_1",
  "error_code": "RESUME_NOT_FOUND",
  "timestamp": "2024-01-15T10:30:00Z",
  "details": {
    "unique_key": "john_doe_1"
  }
}
```

### Interview Service (2000-2999)

```typescript
enum InterviewErrorCode {
  INTERVIEW_GENERATION_FAILED = "INTERVIEW_GENERATION_FAILED", // 2001
  INTERVIEW_NOT_FOUND = "INTERVIEW_NOT_FOUND",                 // 2002
  INTERVIEW_TASK_FAILED = "INTERVIEW_TASK_FAILED",             // 2003
  INTERVIEW_LLM_ERROR = "INTERVIEW_LLM_ERROR"                  // 2004
}
```

**예시 응답:**
```json
{
  "detail": "LLM provider 'openai' error: Rate limit exceeded",
  "error_code": "INTERVIEW_LLM_ERROR",
  "timestamp": "2024-01-15T10:30:00Z",
  "details": {
    "provider": "openai",
    "llm_error": "Rate limit exceeded"
  }
}
```

### Learning Service (3000-3999)

```typescript
enum LearningErrorCode {
  LEARNING_PATH_GENERATION_FAILED = "LEARNING_PATH_GENERATION_FAILED", // 3001
  LEARNING_PATH_NOT_FOUND = "LEARNING_PATH_NOT_FOUND",                 // 3002
  LEARNING_TASK_FAILED = "LEARNING_TASK_FAILED",                       // 3003
  LEARNING_LLM_ERROR = "LEARNING_LLM_ERROR"                            // 3004
}
```

### LLM Service (4000-4999)

```typescript
enum LLMErrorCode {
  LLM_PROVIDER_NOT_AVAILABLE = "LLM_PROVIDER_NOT_AVAILABLE", // 4001
  LLM_API_RATE_LIMIT = "LLM_API_RATE_LIMIT",                 // 4002
  LLM_API_TIMEOUT = "LLM_API_TIMEOUT",                       // 4003
  LLM_RESPONSE_PARSING_ERROR = "LLM_RESPONSE_PARSING_ERROR", // 4004
  LLM_INVALID_RESPONSE = "LLM_INVALID_RESPONSE"              // 4005
}
```

### Database Errors (5000-5999)

```typescript
enum DatabaseErrorCode {
  DATABASE_CONNECTION_ERROR = "DATABASE_CONNECTION_ERROR", // 5001
  DATABASE_OPERATION_FAILED = "DATABASE_OPERATION_FAILED", // 5002
  DATABASE_TIMEOUT = "DATABASE_TIMEOUT"                    // 5003
}
```

### Celery/Queue Errors (6000-6999)

```typescript
enum CeleryErrorCode {
  TASK_QUEUE_ERROR = "TASK_QUEUE_ERROR",           // 6001
  TASK_EXECUTION_FAILED = "TASK_EXECUTION_FAILED", // 6002
  TASK_TIMEOUT = "TASK_TIMEOUT",                   // 6003
  TASK_RETRY_EXHAUSTED = "TASK_RETRY_EXHAUSTED"    // 6004
}
```

## 구현 예시

### Python (FastAPI) 사용법

```python
from shared.utils.error_handler import ResumeErrors, InterviewErrors

# Resume 서비스에서
@router.get("/{unique_key}")
async def get_resume(unique_key: str):
    try:
        resume = await get_resume_by_unique_key(unique_key)
        if not resume:
            raise ResumeErrors.not_found(unique_key)
        return resume
    except Exception as e:
        if hasattr(e, 'error_code'):  # APIError인 경우
            raise
        raise ResumeErrors.creation_failed(str(e))

# Interview 서비스에서
@router.post("/{unique_key}/questions")
async def generate_questions(unique_key: str):
    try:
        result = await generate_interview_questions_service(unique_key)
        return result
    except Exception as e:
        if "Resume not found" in str(e):
            raise ResumeErrors.not_found(unique_key)
        raise InterviewErrors.generation_failed(unique_key, str(e))
```

## 에러 모니터링

### 로그 형식

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "ERROR",
  "service": "interview-service",
  "error_code": "INTERVIEW_LLM_ERROR",
  "message": "LLM provider 'openai' error: Rate limit exceeded",
  "details": {
    "unique_key": "user_123",
    "provider": "openai",
    "request_id": "req_abc123",
    "stack_trace": "..."
  }
}
```

