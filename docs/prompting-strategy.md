# 프롬프팅 전략

> AI Challenge API의 고도화된 프롬프트 엔지니어링 전략

## 목표: 개인 맞춤형의 특징 살리기

### 전체 시스템 개요:
이력서 정보를 바탕으로 **면접 질문 생성**과 **학습 경로 추천** 두 가지 핵심 기능을 제공합니다.

### 공통 프롬프트 전략:
1. **개인맞춤형 근거 제시**: 각 질문과 학습 경로의 제시 이유를 구체적으로 설명
2. **실무 중심 접근**: 이론적 지식보다 실제 업무 경험과 문제해결 능력 중심
3. **프롬프트 실험 및 최적화**: Playground에서 다양한 프롬프트 패턴을 반복 실험하여 최적화

---

# 1️⃣ 면접 질문 생성 프로세스

## 프로세스 플로우:
```
이력서 분석 → 질문 유형 선정 → 개인맞춤 질문 생성 → 품질 검증 → 5개 질문 출력
```

## 핵심 전략:

### **다차원 질문 유형 체계**

<details>
<summary>8가지 질문 유형 체계</summary>

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

### **실무 시나리오 기반 질문 설계**
- **운영 상황 시뮬레이션**: "실제 서비스 운영 중 ○○ 장애 발생 시..." 
- **확장성 검증**: "트래픽 10배 증가 시 병목 지점과 해결 전략..."
- **의사결정 과정 탐구**: "기술 선택의 근거와 대안 검토 과정..."

### **프로젝트 심층 분석 방향**
- **구현 세부사항**: "단순히 Redis 사용이 아닌 어떤 데이터 구조를 어떻게 활용했는지"
- **기술적 도전**: "마이크로서비스 간 데이터 일관성 보장 방법"
- **성과 측정**: "Virtual Thread 도입으로 어떤 메트릭이 얼마나 개선되었는지"

## 면접 질문 생성 성과

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

---

# 2️⃣ 학습 경로 추천 프로세스

## 프로세스 플로우:
```
이력서 분석 → 장점/단점 식별 → 학습 우선순위 설정 → 개인맞춤 학습 경로 생성 → 3-8개 경로 출력
```

## 핵심 전략:

### **3단계 체계적 분석**

<details>
<summary>장점/단점 분석 프로세스</summary>

**1단계: 장점 식별**
- 프로젝트 성과 및 기술적 차별화 포인트 분석
- 경력 대비 뛰어난 기술 활용도 평가
- 업계에서 인정받을 만한 경험 및 성취 파악

**2단계: 단점 식별**
- 경력 수준 대비 부족한 기술 영역 진단
- 현재 시장 요구사항과의 Gap 분석
- 향후 성장을 위해 보완이 필요한 역량 파악

**3단계: 학습 방향 설정**
- **강점 심화**: 이미 보유한 강점을 전문성 수준으로 발전
- **약점 보완**: 부족한 영역을 시장 요구 수준으로 향상
- **균형잡힌 조합**: 강점 60% + 약점 보완 40% 비율

</details>

### **학습 경로 구조화**

각 학습 경로는 다음 정보를 포함합니다:
- **Type**: `strength` (강점 심화) 또는 `weakness` (약점 보완)
- **Title**: 구체적인 학습 주제
- **Description**: 학습 목표 및 예상 성과
- **Reason**: 해당 학습을 추천하는 개인맞춤형 근거
- **Resources**: 추천 학습 방법 및 리소스
- **Link**: 관련 학습 자료 링크

## 학습 경로 추천 성과

**개선 전 vs 개선 후:**
- **기존**: "Spring Boot 공부하세요" (일반적 추천)
- **개선**: "이미 Spring Boot 기반 MSA 구축 경험이 뛰어나므로, Spring Cloud Gateway 기반 API Gateway 패턴 전문성을 강화하여 아키텍트 역량 발전" (개인맞춤형 근거)

---

# 3️⃣ 공통 구현 방법론

## 프롬프트 구조화 방법론

### YAML 기반 프롬프트 관리
```yaml
# interview-service/prompts/interview_questions.yaml
name: "interview_questions_generation"
version: "3.0.0"
description: "백엔드 개발자 대상 개인 맞춤형 기술 면접 질문 생성 프롬프트"

guidelines:
  - 목적: 지원자의 실무 역량·문제 해결력을 검증하는 '개인 맞춤형' 질문을 생성한다.
  - 입력: 이력서 JSON(경력, 프로젝트, 기술 스택).
  - 출력: JSON 스키마에 맞춘 5개의 질문 세트.

system_prompt_template: |
  당신은 백엔드 개발자 채용 전문 기술 면접관입니다.
  주어진 이력서 정보를 바탕으로 지원자의 실무 역량과 문제 해결력을 검증하는 개인 맞춤형 면접 질문 5개를 생성해주세요.

human_prompt_template: |
  지원자 정보:
  이름: {name}
  경력: {experience_months}개월
  
  프로젝트 경험:
  {projects}
  
  위 프로젝트 경험을 바탕으로 실제 면접에서 나올 법한 다양한 유형의 질문 5개를 생성해주세요.

output_schema:
  questions:
    - difficulty: string     # easy|medium|hard
      topic: string          # 주요 기술 키워드
      type: string           # 8가지 질문 유형 중 하나
      question: string       # 실제 질문 본문
      what_good_answers_cover: [string]   # 좋은 답변이 포함해야 할 핵심 요소
```

### Few-Shot Learning 적용
```yaml
examples:
  - input:
      name: "김개발"
      tech_stack: ["Spring Boot", "Redis", "MySQL"]
      project: "커머스 API 개발"
    output:
      question: "Spring Boot 기반 커머스 API에서 Redis를 캐시로 활용하실 때, 캐시 무효화 전략은 어떻게 설계하셨나요? 특히 상품 정보 업데이트 시 일관성을 어떻게 보장하셨는지..."
      type: "Implementation"
      difficulty: "medium"
```

### JSON Schema 강제
```yaml
response_format:
  type: "json_object"
  schema:
    type: "object"
    properties:
      questions:
        type: "array"
        items:
          type: "object"
          properties:
            difficulty: { "type": "string", "enum": ["easy", "medium", "hard"] }
            topic: { "type": "string" }
            type: { "type": "string" }
            question: { "type": "string" }
          required: ["difficulty", "topic", "type", "question"]
    required: ["questions"]
```

## Chain-of-Thought 추론

### 단계별 추론 과정
```
1. 이력서 분석: 
   - 기술 스택 파악
   - 프로젝트 복잡도 평가
   - 경력 수준 확인

2. 질문 카테고리 선정:
   - 8가지 유형 중 적합한 5가지 선택
   - 난이도 분배 (easy:1, medium:3, hard:1)

3. 개인맞춤화:
   - 구체적 프로젝트 경험 언급
   - 실무 상황 시뮬레이션
   - 기술적 의사결정 과정 탐구

4. 품질 검증:
   - 질문 다양성 확인
   - 실무 적합성 검토
   - 개인맞춤성 정도 평가
```

## 동적 난이도 조정

### 경력별 난이도 매트릭스
```python
DIFFICULTY_MATRIX = {
    "junior": {  # 0-24개월
        "easy": 2,
        "medium": 2, 
        "hard": 1
    },
    "mid": {     # 24-60개월
        "easy": 1,
        "medium": 3,
        "hard": 1
    },
    "senior": {  # 60개월+
        "easy": 0,
        "medium": 2,
        "hard": 3
    }
}
```

### 기술 스택 복잡도 가중치
```python
TECH_COMPLEXITY_WEIGHT = {
    "basic": ["HTML", "CSS", "JavaScript"],           # +0
    "intermediate": ["React", "Node.js", "MySQL"],    # +1
    "advanced": ["Kubernetes", "Kafka", "Redis"],     # +2
    "expert": ["Istio", "Consul", "Elasticsearch"]    # +3
}
```

