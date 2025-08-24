# LLM 통합 가이드

> 다중 LLM 모델 통합 및 폴백 전략

## 다중 모델 지원 현황

### 구현된 LLM Provider들:

| Provider | 모델명 | 특징 | 토큰당 가격 | 기본 모델 |
|----------|--------|------|-------------|----------|
| **Gemini** | `gemini-2.5-flash` | 무료, 빠른 처리, 기본 모델 | 무료 | **기본** |
| **OpenAI** | `gpt-4.1` | 빠른 응답, 일관성 있는 품질 | $0.0015/1K tokens | 폴백 1순위 |
| **Claude** | `claude-3-5-sonnet-20241022` | 창의적이고 상세한 응답 | $0.003/1K tokens | 폴백 2순위 | 

### 한 이력서당 예상 비용:
- **면접 질문 생성**: ~500 토큰 사용
  - OpenAI: $0.00075
  - Claude: $0.0015
  - Gemini: 무료
- **학습 경로 생성**: ~800 토큰 사용
  - OpenAI: $0.0012
  - Claude: $0.0024
  - Gemini: 무료

## 우선순위 및 폴백 전략

### 구현된 LLM Registry 시스템:

<details>
<summary>LLM Registry 구현 코드</summary>

```python
# backend/shared/llm/registry.py 
class LLMRegistry:
    def register(self, name: str, client_class: Type[LLMClient])
    def create_client(self, name: str) -> Optional[LLMClient]
    def get_client(self, name: str) -> Optional[LLMClient]
    def get_client_with_fallback(self) -> Optional[LLMClient]
    def get_available_clients(self) -> List[str]

registry = LLMRegistry()
preferred_order = ["gemini", "openai", "claude"]
```

</details>

### 폴백 시나리오
1. **기본 모델 (Gemini)** → 무료 모델로 먼저 시도
2. **자동 폴백 체인** → 실패 시 Gemini → OpenAI → Claude 순서로 시도
3. **모든 Provider 실패** → 명확한 에러 메시지와 함께 HTTP 500 반환

### 모델 관리 
- **Provider Registry**: 새로운 LLM 추가 시 최소 코드 변경 (현재 OpenAI, Claude, Gemini 운영)
- **설정 기반**: 환경변수로 모델별 파라미터 조정 (API키, 온도, 토큰수, 타임아웃)
- **추상화 계층**: LLMClient 베이스 클래스로 일관된 인터페이스 제공
-  **실시간 폴백**: Provider 장애 시 1초 내 자동 전환

## LangChain 활용
- **추상화**: 다양한 LLM Provider 통합 인터페이스 (OpenAI, Claude, Gemini)
- **메시지 체인**: SystemMessage + HumanMessage로 구조화된 프롬프트
- **스트리밍**: 실시간 응답 스트리밍 지원 (`ainvoke`, `astream` 메소드)
- **에러 핸들링**: 폴백 설정으로 LLM Provider 장애시에도 안정적으로 서비스 제공 가능
- **비동기 처리**: async/await 패턴으로 동시 처리 최적화

## 설정 및 환경 변수

### 필수 환경 변수
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Claude
CLAUDE_API_KEY=sk-ant-...

# Gemini
GEMINI_API_KEY=AI...

# MongoDB
MONGODB_URL=mongodb://localhost:27017/ai_challenge
```

### LLM 클라이언트 설정
```python
# shared/llm/openai_client.py
class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = ChatOpenAI(
            model="gpt-4-1106-preview",
            temperature=0.7,
            max_tokens=1500,
            timeout=30
        )

# shared/llm/claude_client.py  
class ClaudeClient(LLMClient):
    def __init__(self):
        self.client = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=1500,
            timeout=30
        )

# shared/llm/gemini_client.py
class GeminiClient(LLMClient):
    def __init__(self):
        self.client = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            max_tokens=1500,
            timeout=30
        )
```

## 에러 처리 및 재시도

### LLM 호출 에러 처리
```python
async def call_llm_with_fallback(messages: List[BaseMessage]) -> str:
    """LLM 호출 with 폴백 전략"""
    providers = ["gemini", "openai", "claude"]
    
    for provider in providers:
        try:
            client = get_llm_client(provider)
            response = await client.ainvoke(messages)
            return response.content
            
        except RateLimitError:
            logger.warning(f"{provider} rate limited, trying next provider")
            continue
            
        except APIConnectionError:
            logger.warning(f"{provider} connection failed, trying next provider")
            continue
            
        except Exception as e:
            logger.error(f"{provider} failed: {e}")
            continue
    
    raise LLMServiceUnavailableError("All LLM providers failed")
```

### 재시도 메커니즘
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def generate_with_retry(prompt: str, provider: str = "gemini") -> str:
    """재시도 로직을 포함한 LLM 호출"""
    client = get_llm_client(provider)
    response = await client.ainvoke([HumanMessage(content=prompt)])
    return response.content
```

## 모니터링 및 로깅

### LLM 사용량 추적
```python
class LLMUsageTracker:
    def __init__(self):
        self.usage_stats = defaultdict(int)
    
    def track_request(self, provider: str, tokens: int, cost: float):
        self.usage_stats[f"{provider}_requests"] += 1
        self.usage_stats[f"{provider}_tokens"] += tokens
        self.usage_stats[f"{provider}_cost"] += cost
    
    def get_daily_stats(self) -> Dict[str, Any]:
        return dict(self.usage_stats)
```

### 응답 시간 모니터링
```python
import time
from functools import wraps

def monitor_llm_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"LLM call succeeded in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"LLM call failed after {duration:.2f}s: {e}")
            raise
    return wrapper
```

## 최적화 전략

### 1. 비용 최적화
- **Gemini 우선 사용**: 무료 모델로 비용 절감
- **스마트 라우팅**: 요청 복잡도에 따른 모델 선택

### 2. 성능 최적화
- **비동기 처리**: 동시 여러 요청 처리
- **커넥션 풀링**: HTTP 연결 재사용
- **타임아웃 관리**: 응답 시간 기반 폴백

### 3. 신뢰성 확보
- **헬스체크**: 각 Provider의 상태 모니터링
- **자동 폐일오버**: 장애 시 즉시 다른 Provider로 전환
- **로깅**: 상세한 요청/응답 로그 기록
