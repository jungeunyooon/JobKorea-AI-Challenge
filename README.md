#  AI Challenge: 이력서 기반 맞춤형 커리어 코치 챗봇 API

> **구직자의 이력서를 분석하여 개인 맞춤형 면접 질문과 학습 경로를 제공하는 지능형 백엔드 API**

## 프로젝트 개요

구직자가 입력한 이력서 핵심 정보(경력, 직무, 기술 스킬)를 바탕으로 생성형 AI가 **실제 면접에서 나올 법한 심층적인 질문 5개**와 **개인 맞춤형 학습 경로**를 생성하여 구직자의 합격률 향상을 돕는 백엔드 서비스입니다.

---

## 요구사항

### 1. 이력서 핵심 정보 입력
- **API 엔드포인트**: `POST /api/v1/resumes/`
- **입력 형태**: JSON
- **지원 정보**: 경력 요약, 수행 직무, 보유 기술 스킬, 경력 연수


<details>
<summary>예시 입력</summary>

```json
{
  "name": "김개발",
  "summary": "3년차 백엔드 개발자로 Spring Boot 기반 마이크로서비스 개발 경험",
  "contact_info": {
    "email": "kim.dev@example.com",
    "github": "https://github.com/kimdev",
    "phone": "010-1234-5678"
  },
  "work_experiences": [
    {
      "company": "테크스타트업",
      "position": "백엔드 개발자",
      "duration": "2022.01 ~ 현재",
      "project_name": "커머스 플랫폼 API 개발",
      "tech_stack": ["Java", "Spring Boot", "MySQL", "Redis", "AWS"],
      "achievements": [
        "MSA 기반 주문/결제 시스템 설계 및 구현",
        "Redis 캐싱으로 API 응답 속도 50% 개선"
      ]
    }
  ],
  "personal_projects": [
    {
      "name": "실시간 채팅 서비스",
      "description": "WebSocket 기반 실시간 채팅 플랫폼",
      "tech_stack": ["Spring Boot", "WebSocket", "PostgreSQL", "Docker"],
      "key_achievements": [
        "동시 접속자 1000명 처리 가능한 채팅 시스템 구현",
        "Docker 컨테이너화로 배포 자동화"
      ]
    }
  ],
  "technical_skills": {
    "programming_languages": ["Java", "Python"],
    "frameworks": ["Spring Boot", "Spring Security"],
    "databases": ["MySQL", "PostgreSQL", "Redis"],
    "cloud_platforms": ["AWS EC2", "AWS RDS"],
    "devops_tools": ["Docker", "GitHub Actions"]
  },
  "total_experience_months": 36
}
```

</details>

### 2. 맞춤형 면접 질문 생성
- **API 엔드포인트**: `POST /api/v1/interview/{unique_key}/questions`
- **생성 개수**: 5개의 심층적인 면접 질문
- **다중 생성**: 같은 이력서로 여러 번 생성 가능
- **LLM 선택**: `?provider=openai|claude|gemini` 파라미터 지원
- **카테고리화**: 기술/경험/문제해결/인성 등으로 구분
- **난이도 설정**: 초급/중급/고급 난이도 자동 배정

### 3. 개인 맞춤형 학습 경로 생성
- **API 엔드포인트**: `POST /api/v1/learning/{unique_key}/learning-path`
- **생성 개수**: 5~8개의 구체적인 학습 경로
- **상세 정보**: 카테고리, 우선순위, 예상 기간, 추천 리소스 포함
- **실용성**: 구체적이고 실행 가능한 방안 제시

---

## 백엔드 아키텍처 및 구현

### 시스템 아키텍처 

![Architecture](Architecture.png)

### 도메인 설정

#### **개발 환경 (현재 설정)**
- **API Gateway 주소**: `http://api.localhost`
- **Hosts 파일 설정 필요**: `/etc/hosts`에 `127.0.0.1 api.localhost` 추가
- api.localhost는 개발을 위한 설정이기 때문에 추후 도메인 연결이 필요합니다. 
- **서비스 접근**:
  - Resume API: http://api.localhost/api/v1/resumes/docs
  - Interview API: http://api.localhost/api/v1/interview/docs  
  - Learning API: http://api.localhost/api/v1/learning/docs
  - Traefik Dashboard: http://localhost:8080


### 아키텍처 구성 요소

####  **마이크로서비스 (FastAPI)**
- **Resume Service (Port 8001)**: 이력서 CRUD 관리
- **Interview Service (Port 8002)**: AI 기반 면접 질문 생성
- **Learning Service (Port 8003)**: AI 기반 학습 경로 생성

#### **Shared Module**
- **LLM Registry**: 다중 AI 모델 관리 및 폴백 처리
- **Database Connection**: MongoDB 연결 풀 관리
- **Common Utilities**: 공통 로깅, 에러 처리, 설정 관리

####  **데이터 레이어**
- **MongoDB**: 유연한 스키마로 다양한 이력서 형태 지원
- **Collections**: resumes, interviews, learning_paths

####  **AI 레이어**
- **OpenAI GPT-3.5**: 빠르고 일관된 품질의 기본 모델
- **Claude 3.5 Sonnet**: 창의적이고 상세한 고품질 응답
- **Gemini 1.5 Flash**: 무료 모델로 비용 최적화

#### **인프라 레이어**
- **Docker Compose**: 로컬 개발 환경 통합 관리
- **API Gateway** (향후): Traefik 기반 라우팅 및 로드밸런싱

### 데이터 흐름 (Data Flow)

1. **이력서 등록**: Client → Resume Service → MongoDB
2. **면접 질문 생성**: Client → Interview Service → LLM → MongoDB
3. **학습 경로 생성**: Client → Learning Service → LLM → MongoDB
4. **폴백 처리**: LLM 실패 시 자동으로 다른 Provider로 전환

### 기술 스택 선정 이유

#### **FastAPI (Python)**
- **비동기 처리**: async/await 지원으로 I/O 바운드 작업 최적화
- **생태계**: LangChain, OpenAI SDK 등 AI 라이브러리와 완벽 호환

#### **MongoDB**
- **스키마 유연성**: 다양한 형태의 이력서 데이터 저장
- **JSON 친화적**: FastAPI와 자연스러운 통합
- **확장성**: 샤딩 및 레플리카셋 지원

### 확장성을 고려한 아키텍처 설계: MSA

#### 현재 구현된 마이크로서비스 구조:

<details>
<summary> MSA 폴더 구조</summary>

```
📁 backend/
├── shared/                    # 공통 모듈
│   ├── config/base.py            # 통합 설정 관리
│   ├── database/connection.py    # MongoDB 연결 관리
│   ├── llm/                      # LLM 클라이언트 추상화
│   │   ├── base.py              # 추상 기본 클래스
│   │   ├── openai_client.py     # OpenAI GPT 클라이언트
│   │   ├── claude_client.py     # Anthropic Claude 클라이언트
│   │   ├── gemini_client.py     # Google Gemini 클라이언트
│   │   └── registry.py          # LLM 레지스트리 & 폴백
│   └── utils/                   # 공통 유틸리티
│
├── resume-service/            # 이력서 관리 서비스
│   ├── src/routes.py            # REST API 엔드포인트
│   ├── src/crud.py              # 데이터베이스 CRUD
│   └── main.py                  # 서비스 엔트리포인트
│
├── interview-service/         # 면접 질문 생성 서비스
│   ├── src/routes.py            # REST API 엔드포인트
│   ├── src/service.py           # 비즈니스 로직
│   ├── src/crud.py              # 데이터베이스 CRUD
│   └── main.py                  # 서비스 엔트리포인트
│
└── learning-service/          # 학습 경로 생성 서비스
    ├── src/routes.py            # REST API 엔드포인트
    ├── src/service.py           # 비즈니스 로직
    └── main.py                  # 서비스 엔트리포인트
```

</details>

#### MSA 설계 원칙:
1. **단일 책임**: 각 서비스는 하나의 비즈니스 도메인만 담당
2. **데이터 독립성**: 각 서비스가 독립적인 데이터베이스 접근
3. **API 게이트웨이**: 향후 Traefik 또는 Kong 도입 예정
4. **서비스간 통신**: REST API 기반 (향후 gRPC 고려)
5. **공통 모듈**: shared 폴더로 코드 재사용성 극대화

### 테스트 전략

#### **Given-When-Then 패턴**

<details>
<summary> BDD 테스트 예시</summary>

```python
def test_generate_interview_questions():
    # Given: 유효한 이력서 데이터가 주어지고
    resume_data = {"name": "김개발", "tech_skills": ["Python", "FastAPI"]}
    
    # When: 면접 질문 생성을 요청하면 (Gemini 기본 사용)
    response = client.post(f"/interview/{unique_key}/questions")
    
    # Then: 5개의 면접 질문이 생성된다
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 5
    assert all("question" in q for q in response.json()["questions"])
```

</details>

#### **Table Driven Test**
다양한 시나리오를 효율적으로 테스트:

<details>
<summary 파라미터화된 테스트 예시</summary>

```python
@pytest.mark.parametrize("unique_key,resume_type,expected_questions", [
    ("test_junior", "신입개발자", 5),
    ("test_senior", "시니어개발자", 5),
    ("test_fullstack", "풀스택개발자", 5),
    ("invalid_key", "존재하지_않는_키", None),
])
def test_resume_based_question_generation(unique_key, resume_type, expected_questions):
    # Given: 다양한 유형의 이력서가 주어지고
    # When: 면접 질문 생성을 요청하면 (Gemini 기본 사용)
    response = client.post(f"/interview/{unique_key}/questions")
    
    # Then: 예상된 결과를 반환한다
    if expected_questions:
        assert response.status_code == 200
        assert len(response.json()["questions"]) == expected_questions
        assert response.json()["provider"] == "gemini"
    else:
        assert response.status_code == 404
```

</details>

#### **Flaky Test 대응 전략**

<details>
<summary>Flaky Test 대응 전략</summary>

##### **자동 재실행 (Rerun)**
```python
# pytest-rerunfailures 사용
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_llm_api_call():
    """LLM API 호출 테스트 - 네트워크 이슈로 인한 실패 시 재시도"""
    response = client.post("/interview/test_user/questions")
    assert response.status_code == 200
    assert response.json()["provider"] in ["gemini", "openai", "claude"]  # 폴백 허용
```

##### **병렬 실행 (Parallel)**
```python
# pytest-xdist 사용
# 테스트 실행: pytest -n auto (CPU 코어 수만큼 병렬 실행)

@pytest.mark.parametrize("unique_key", [
    "user1_1", "user2_1", "user3_1", "user4_1", "user5_1"
])
def test_concurrent_interview_generation(unique_key):
    """동시 다발적 면접 질문 생성 테스트"""
    response = client.post(f"/interview/{unique_key}/questions")
    assert response.status_code == 200
```

##### **Timeout 및 Retry 로직**
```python
@pytest.mark.timeout(30)  # 30초 타임아웃
@pytest.mark.retry(max_attempts=3, backoff=1.5)
def test_learning_path_generation():
    """학습 경로 생성 테스트 - 타임아웃 및 재시도"""
    response = client.post("/learning/test_user/learning-path")
    assert response.status_code == 200
```

</details>

## 선정된 llm 모델 및 전략

### 다중 모델 지원 현황

#### 구현된 LLM Provider들:

| Provider | 모델명 | 특징 | 토큰당 가격 | 기본 모델 |
|----------|--------|------|-------------|----------|
| **Gemini** | `gemini-2.5-flash` | 무료, 빠른 처리, 기본 모델 | 무료 | **기본** |
| **OpenAI** | `gpt-4.1` | 빠른 응답, 일관성 있는 품질 | $0.0015/1K tokens | 폴백 1순위 |
| **Claude** | `claude-3-5-sonnet-20241022` | 창의적이고 상세한 응답 | $0.003/1K tokens | 폴백 2순위 | 

#### 한 이력서당 예상 비용:
- **면접 질문 생성**: ~500 토큰 사용
  - OpenAI: $0.00075
  - Claude: $0.0015
  - Gemini: 무료
- **학습 경로 생성**: ~800 토큰 사용
  - OpenAI: $0.0012
  - Claude: $0.0024
  - Gemini: 무료

### 우선순위 및 폴백 전략

#### 구현된 LLM Registry 시스템:

<details>
<summary> LLM Registry 구현 코드</summary>

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

#### 폴백 시나리오
1. **기본 모델 (Gemini)** → 무료 모델로 먼저 시도
2. **자동 폴백 체인** → 실패 시 Gemini → OpenAI → Claude 순서로 시도
3. **모든 Provider 실패** → 명확한 에러 메시지와 함께 HTTP 500 반환

#### 모델 관리 
- **Provider Registry**: 새로운 LLM 추가 시 최소 코드 변경 (현재 OpenAI, Claude, Gemini 운영)
- **설정 기반**: 환경변수로 모델별 파라미터 조정 (API키, 온도, 토큰수, 타임아웃)
- **추상화 계층**: LLMClient 베이스 클래스로 일관된 인터페이스 제공
-  **실시간 폴백**: Provider 장애 시 1초 내 자동 전환


#### LangChain 활용
- **추상화**: 다양한 LLM Provider 통합 인터페이스 (OpenAI, Claude, Gemini)
- **메시지 체인**: SystemMessage + HumanMessage로 구조화된 프롬프트
- **스트리밍**: 실시간 응답 스트리밍 지원 (`ainvoke`, `astream` 메소드)
- **에러 핸들링**: Provider별 예외 처리 및 자동 재시도
- **비동기 처리**: async/await 패턴으로 동시 처리 최적화

---

## 프롬프팅 전략

### 목표: 개인 맞춤형의 특징 살리기

#### 현재 구현된 프롬프트 전략:

1. **다차원 질문 유형 분석**: 8가지 면접 질문 유형으로 종합적 역량 검증
2. **실무 시나리오 기반**: 실제 운영 상황과 장애 대응 중심의 질문 설계
3. **프로젝트 심층 분석**: 단순 기술 사용이 아닌 구현 세부사항과 의사결정 과정 탐구
4. **장점/단점 체계적 분석**: 이력서 기반 강점 심화 + 약점 보완 학습 경로 생성
5. **개인맞춤형 근거 제시**: 각 질문과 학습 경로의 제시 이유를 구체적으로 설명

#### 면접 질문 프롬프트 예시:

<details>
<summary> 프롬프트 엔지니어링 예시</summary>

```
당신은 경험이 풍부한 기술 면접관입니다.
다음 이력서 정보를 바탕으로 실제 면접에서 나올 법한 심층적인 질문 5개를 생성해주세요.

이력서 정보:
- 이름: {name}
- 경력: {career_summary}
- 주요 업무: {job_roles}
- 기술 스택: {tech_skills}
- 경력 연수: {years_experience}년

요구사항:
1. 지원자의 실제 경험을 바탕으로 한 구체적인 질문
2. 단순한 지식 확인이 아닌 문제해결 능력 평가
3. 각 질문은 카테고리(기술/경험/문제해결/인성)와 난이도(초급/중급/고급) 포함
```

</details>

### 구현된 고도화된 프롬프팅 최적화:

#### 1. **다차원 면접 질문 생성 (Interview Service v3.0)**

<details>
<summary> 8가지 질문 유형 체계</summary>

**구현된 질문 유형들:**
1. **Implementation**: 구체적 구현 방법 (예: "WebSocket 연결 상태 관리를 어떻게 구현하셨나요?")
2. **Trade-off**: 설계 결정과 트레이드오프 (예: "Spring Cloud Gateway vs Nginx 선택 기준은?")
3. **Performance**: 성능 최적화 경험 (예: "Virtual Thread 도입 후 성능 지표 변화는?")
4. **Reliability**: 장애 대응과 안정성 (예: "Redis 다운 시 실시간 채팅 영향과 대응 방안은?")
5. **Scalability**: 확장성과 운영 (예: "동시 사용자 10배 증가 시 병목과 해결책은?")
6. **Quality**: 코드 품질과 테스트 (예: "비동기 메시지 처리 테스트 전략은?")
7. **Collaboration**: 협업과 의사결정 (예: "MSA API 스펙 팀 협의 과정은?")
8. **Business**: 비즈니스 이해도 (예: "실시간 채팅이 매칭 플랫폼에 핵심인 이유는?")

**Before vs After:**
- **기존**: "Kafka를 왜 사용하셨나요?" (단순 기술 질문)
- **개선**: "Kafka 토픽 설계와 Consumer group 구성 기준, 데이터 유실 방지 방안은?" (실무 구현 세부사항)

</details>

#### 2. **장점/단점 체계적 분석 기반 학습 경로 (Learning Service v2.0)**

<details>
<summary>체계적 이력서 분석 프로세스</summary>

**3단계 분석 과정:**
1. **장점 식별**: 프로젝트 성과, 기술 활용도, 차별화 포인트 분석
2. **단점 식별**: 경력 대비 부족 영역, 시장 요구사항 gap 파악
3. **학습 방향 설정**: 강점 심화 + 약점 보완 학습 경로 생성

**응답 구조 개선:**
```json
{
  "analysis": {
    "strengths": ["장점1: 구체적 근거", "장점2: 구체적 근거"],
    "weaknesses": ["단점1: 구체적 근거", "단점2: 구체적 근거"]
  },
  "learning_paths": [
    {
      "type": "strength",  // 강점 심화
      "title": "Kafka 고급 스트리밍 아키텍처",
      "reason": "이미 Kafka+MSA 경험이 뛰어나므로 전문성 강화"
    },
    {
      "type": "weakness",  // 약점 보완
      "title": "분산 시스템 모니터링 구축",
      "reason": "운영 및 장애 대응 경험 부족으로 보완 필요"
    }
  ]
}
```

</details>

#### 3. **실무 시나리오 기반 질문 설계**
- **운영 상황 시뮬레이션**: "실제 서비스 운영 중 ○○ 장애 발생 시..." 
- **확장성 검증**: "트래픽 10배 증가 시 병목 지점과 해결 전략..."
- **의사결정 과정 탐구**: "기술 선택의 근거와 대안 검토 과정..."

#### 4. **프로젝트 심층 분석 방향**
- **구현 세부사항**: "단순히 Redis 사용이 아닌 어떤 데이터 구조를 어떻게 활용했는지"
- **기술적 도전**: "마이크로서비스 간 데이터 일관성 보장 방법"
- **성과 측정**: "Virtual Thread 도입으로 어떤 메트릭이 얼마나 개선되었는지"

#### 5. **실제 테스트 성과**

<details>
<summary>실제 생성된 질문 예시</summary>

**Before (기존 단순 패턴):**
```
- "Kafka를 왜 사용하셨나요?"
- "Redis의 장점이 무엇인가요?"
```

**After (개선된 다차원 질문):**
```
1. Implementation: "Kafka의 토픽 설계는 어떻게 하셨고, Consumer group은 어떤 기준으로 구성하셨나요? 데이터가 유실되지 않도록 어떤 방안을 적용하셨는지..."

2. Trade-off: "모놀리식 아키텍처 대신 MSA를 선택하신 주된 이유는 무엇인가요? MSA 도입으로 인한 복잡성은 어떻게 관리하셨는지..."

3. Reliability: "RabbitMQ 서버가 예기치 않게 다운되면 크롤링 요청들은 어떻게 되며, 어떤 복구 전략을 설계하셨나요?"
```

**품질 개선 지표:**
- 질문 다양성: 단일 패턴 → 8가지 유형 골고루 분포
- 실무 적합성: 이론적 질문 → 실제 경험 검증 질문
- 개인맞춤성: 일반적 질문 → 구체적 프로젝트 기반 질문

</details>

### 추후 프롬프팅 개선 반향

####  **Chain-of-Thought**
- 질문 생성 과정의 추론 단계 명시
- "왜 이 질문이 중요한가" 설명 포함

####  **동적 난이도 조정**
- 경력 연수별 자동 난이도 조정 시스템
- 기술 스택 복잡도 기반 질문 깊이 조절

####  **품질 검증 로직**
- A/B 테스트를 통한 프롬프트 성능 비교
- 사용자 피드백 기반 프롬프트 최적화

---

## 코드 일관성과 협업을 위한 AI 활용

#### 규칙 파일 위치:
- `backend/.cursor/rules/`: Cursor IDE 규칙
- 향후 추가: `.claude/setting.json`, `copilot-instructions.md`

#### `.cursor/rules/`
1. **함수형 프로그래밍**: 클래스보다 순수 함수 선호
2. **단일 책임 원칙**: 각 함수는 하나의 명확한 목적
3. **조기 반환**: 에러 조건을 함수 시작 부분에서 처리
4. **명시적 타입 힌트**: 모든 함수에 완전한 타입 애노테이션
5. **모듈화**: 중복 코드 제거 및 재사용 가능한 유틸리티

#### `.claude/setting.json`

<details>
<summary> Claude AI 설정 파일</summary>

```json
{
  "coding_style": {
    "language": "python",
    "framework": "fastapi",
    "architecture": "microservices",
    "patterns": ["dependency_injection", "repository_pattern"]
  },
  "preferences": {
    "async_preferred": true,
    "type_hints_mandatory": true,
    "docstring_style": "google",
    "max_function_length": 50
  }
}
```

</details>

#### `copilot-instructions.md`

<details>
<summary> GitHub Copilot 가이드라인</summary>

```markdown
# GitHub Copilot 사용 가이드라인

## 코드 생성 원칙
1. FastAPI의 의존성 주입 패턴 사용
2. Pydantic 모델로 데이터 검증
3. async/await 패턴 일관성
4. 에러 핸들링은 HTTPException 사용

## 금지 사항
- 동기 방식의 데이터베이스 호출
- 하드코딩된 설정값
- 타입 힌트 누락
```

</details>
---

## 추후 확장성을 위한 고려사항

### 1. 비동기 처리 최적화 (Python GIL 해결)
#### 현재 상황:
- FastAPI의 async/await 활용으로 I/O 바운드 작업 최적화
- LLM API 호출 시 비동기 처리로 동시성 확보

#### 향후 개선 방안:
- **멀티프로세싱**: CPU 집약적 작업을 위한 ProcessPoolExecutor
- **Celery**: 백그라운드 작업 큐 시스템 도입
- **Redis**: 작업 큐 및 캐싱 레이어 추가
- **uvloop**: 기본 asyncio 이벤트 루프 대체

### 2. PDF 파싱 및 멀티모달 AI
#### 구현 계획:

<details>
<summary> PDF 처리 파이프라인</summary>

```python
# PDF 처리 파이프라인
PDF → Text Extraction → Structured Data → LLM Analysis

기술 스택:
- PyMuPDF: PDF 텍스트 추출
- LangChain Document Loaders: 문서 처리
- GPT-4V/Claude Vision: 이미지 기반 이력서 분석
- Tesseract OCR: 스캔된 문서 처리
```

</details>

#### 고려사항:
- **파일 크기 제한**: 10MB 이하로 제한
- **보안**: 업로드된 파일 스캔 및 자동 삭제
- **형식 지원**: PDF, DOC, DOCX, 이미지 파일
- **개인정보 보호**: 민감 정보 자동 마스킹

### 3. LLM Batch 처리
#### 비용 최적화 전략:
```python
# OpenAI Batch API 활용
batch_requests = [
    {"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", ...},
    {"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", ...}
]

# 50% 비용 절감 가능, 24시간 내 처리
```

#### 구현 방향:
- **큐 시스템**: Redis + Celery로 배치 작업 관리
- **스케줄링**: 야간 시간대 배치 처리
- **우선순위**: 실시간 vs 배치 처리 구분

### 4. 검색 기반 신뢰성 (RAG & External Knowledge)
#### RAG (Retrieval Augmented Generation) 구현:
```python
# 지식 베이스 구축
Knowledge Base:
├── 면접 질문 데이터베이스 (10,000+ 실제 면접 질문)
├── 학습 로드맵 데이터베이스 (직무별 커리어 패스)
├── 기업별 면접 스타일 
└── 최신 기술 트렌드 (Stack Overflow, GitHub 등)

검색 → 컨텍스트 제공 → LLM 생성 → 검증
```

#### 외부 API 연동:
- **Perplexity API**: 최신 기술 동향 검색
- **GitHub API**: 트렌딩 기술 스택 분석
- **LinkedIn API**: 실제 채용 공고 분석
- **Stack Overflow API**: 기술별 학습 리소스

### 5. Rate Limiting 및 트래픽 제어
#### 다층 Rate Limiting:
```python
# 사용자별 제한
- 시간당 10회 면접 질문 생성
- 일일 20회 학습 경로 생성

# IP별 제한  
- 분당 100 요청
- 동시 연결 50개

# 전역 제한
- LLM API 호출 분당 1000회
- 응답 시간 모니터링
```

#### 구현 도구:
- **Redis**: 분산 Rate Limiting
- **SlowAPI**: FastAPI Rate Limiting 미들웨어
- **Nginx**: L4 레벨 트래픽 제어

### 6. LLM 비용 최적화 전략
#### 스마트 라우팅:
```python
# 요청 복잡도 기반 모델 선택
def select_model(request_complexity):
    if complexity == "simple":
        return "gemini-1.5-flash"  # 무료
    elif complexity == "medium":
        return "gpt-3.5-turbo"     # 저비용
    else:
        return "claude-3-5-sonnet"  # 고품질
```

#### 캐싱 전략:
- **Redis 캐싱**: 유사한 이력서에 대한 결과 재사용
- **임베딩 기반**: 이력서 유사도 측정 후 캐시 활용
- **TTL 관리**: 시간 기반 캐시 무효화

### 7. 응답 시간 기반 폴백 전략
#### 지능형 폴백:
```python
# 응답 시간 모니터링
avg_response_time = {
    "openai": 2.5,    # 초
    "claude": 4.2,    # 초  
    "gemini": 1.8     # 초
}

# 타임아웃 기반 폴백
if response_time > avg_time * 1.5:
    switch_to_faster_model()
```

#### 성능 지표:
- **P95 응답 시간**: 3초 이내 목표
- **모델별 SLA**: 개별 모델 성능 추적
- **자동 스케일링**: 트래픽 기반 인스턴스 조정
---
