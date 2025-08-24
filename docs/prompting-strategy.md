# 프롬프팅 전략

> AI Challenge API의 고도화된 프롬프트 엔지니어링 전략

## 목표: 개인 맞춤형의 특징 살리기

### 현재 구현된 프롬프트 전략:

1. **다차원 질문 유형 분석**: 8가지 면접 질문 유형으로 종합적 역량 검증
2. **실무 시나리오 기반**: 실제 운영 상황과 장애 대응 중심의 질문 설계
3. **프로젝트 심층 분석**: 단순 기술 사용이 아닌 구현 세부사항과 의사결정 과정 탐구
4. **장점/단점 체계적 분석**: 이력서 기반 강점 심화 + 약점 보완 학습 경로 생성
5. **개인맞춤형 근거 제시**: 각 질문과 학습 경로의 제시 이유를 구체적으로 설명
6. **프롬프트 실험 및 최적화**: Playground에서 다양한 프롬프트 패턴을 반복 실험하여, 질문 설계 및 답변 구조를 최적화

## 면접 질문 프롬프트 예시:

<details>
<summary>프롬프트 엔지니어링 예시</summary>

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

## 구현된 고도화된 프롬프팅 최적화:

### 1. **다차원 면접 질문 생성 (Interview Service v3.0)**

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

### 2. **장점/단점 체계적 분석 기반 학습 경로 (Learning Service v2.0)**

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

### 3. **실무 시나리오 기반 질문 설계**
- **운영 상황 시뮬레이션**: "실제 서비스 운영 중 ○○ 장애 발생 시..." 
- **확장성 검증**: "트래픽 10배 증가 시 병목 지점과 해결 전략..."
- **의사결정 과정 탐구**: "기술 선택의 근거와 대안 검토 과정..."

### 4. **프로젝트 심층 분석 방향**
- **구현 세부사항**: "단순히 Redis 사용이 아닌 어떤 데이터 구조를 어떻게 활용했는지"
- **기술적 도전**: "마이크로서비스 간 데이터 일관성 보장 방법"
- **성과 측정**: "Virtual Thread 도입으로 어떤 메트릭이 얼마나 개선되었는지"

### 5. **실제 테스트 성과**

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
1. **이력서 분석**: 
   - 기술 스택 파악
   - 프로젝트 복잡도 평가
   - 경력 수준 확인

2. **질문 카테고리 선정**:
   - 8가지 유형 중 적합한 5가지 선택
   - 난이도 분배 (easy:1, medium:3, hard:1)

3. **개인맞춤화**:
   - 구체적 프로젝트 경험 언급
   - 실무 상황 시뮬레이션
   - 기술적 의사결정 과정 탐구

4. **품질 검증**:
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

## 추후 프롬프팅 개선 방향

### **Quality Validation**
- A/B 테스트를 통한 프롬프트 성능 비교
- 사용자 피드백 기반 프롬프트 최적화

### **Multi-turn Conversation**
- 면접 질문 → 답변 → 추가 질문 플로우
- 컨텍스트 유지한 연속 대화

### **Domain-Specific Prompts**
- 백엔드/프론트엔드/DevOps별 전문 프롬프트
- 회사 규모별(스타트업/대기업) 맞춤 질문

### **Real-time Adaptation**
- 실시간 답변 분석 후 다음 질문 난이도 조정
- 면접자 반응 기반 질문 스타일 변경
