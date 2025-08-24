# 향후 확장 계획

> AI Challenge API의 확장성을 위한 로드맵 및 기술적 고려사항

## 1. 비동기 처리 실패 전략 및 장애 복구

### Dead Letter Queue (DLQ) 구현:
- **RabbitMQ DLQ**: 실패한 메시지를 별도 큐로 이동하여 데이터 손실 방지
- **Redis DLQ**: 실패 작업의 상세 정보(에러 원인, 재시도 횟수, 원본 데이터) 저장
- **처리 파이프라인**: 원본 큐 → 처리 → 실패 시 재시도 큐 → 최종 실패 시 DLQ

### 재시도 전략:
- **지수 백오프**: 재시도 간격을 점진적으로 증가시켜 시스템 부하 완화
- **에러별 커스텀 로직**: Rate Limit은 5분 후, Service Unavailable은 1분 후 재시도
- **Jitter 적용**: 동시 재시도로 인한 시스템 과부하 방지

### 장애 복구 메커니즘:
- **Circuit Breaker**: LLM 서비스 장애 시 자동 차단 및 폴백
- **Health Check**: 주기적인 서비스 상태 모니터링
- **Graceful Degradation**: 서비스 레벨별 기능 축소 운영
- **Manual Retry**: DLQ의 실패한 작업 수동 재처리

### 모니터링 및 알림:
- **Flower + Prometheus**: 실시간 작업 상태 및 성능 지표 모니터링
- **DLQ 임계치 알림**: 누적된 실패 작업이 임계치 초과 시 Slack 알림
- **SLA 추적**: 작업별 응답 시간 목표 설정 및 모니터링

## 2. PDF 파싱 및 멀티모달 AI

### 구현 계획:

<details>
<summary>PDF 처리 파이프라인</summary>

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

### 고려사항:
- **파일 크기 제한**: 10MB 이하로 제한
- **보안**: 업로드된 파일 스캔 및 자동 삭제
- **형식 지원**: PDF, DOC, DOCX, 이미지 파일
- **개인정보 보호**: 민감 정보 자동 마스킹

## 3. LLM Batch 처리

### 비용 최적화 전략:
```python
# OpenAI Batch API 활용
batch_requests = [
    {"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", ...},
    {"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", ...}
]

# 50% 비용 절감 가능, 24시간 내 처리
```

### 구현 방향:
- **큐 시스템**: Redis + Celery로 배치 작업 관리
- **스케줄링**: 야간 시간대 배치 처리
- **우선순위**: 실시간 vs 배치 처리 구분

## 4. 검색 기반 신뢰성 (RAG & External Knowledge)

### RAG (Retrieval Augmented Generation) 구현:
```python
# 지식 베이스 구축
Knowledge Base:
├── 면접 질문 데이터베이스 (10,000+ 실제 면접 질문)
├── 학습 로드맵 데이터베이스 (직무별 커리어 패스)
├── 기업별 면접 스타일 
└── 최신 기술 트렌드 (Stack Overflow, GitHub 등)

검색 → 컨텍스트 제공 → LLM 생성 → 검증
```

### 외부 API 연동:
- **Perplexity API**: 최신 기술 동향 검색
- **GitHub API**: 트렌딩 기술 스택 분석
- **잡코리아 API**: 실제 채용 공고 분석
- **Stack Overflow API**: 기술별 학습 리소스


## 5. Rate Limiting 및 트래픽 제어

### 다층 Rate Limiting:
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

### 구현 도구:
- **Redis**: 분산 Rate Limiting
- **SlowAPI**: FastAPI Rate Limiting 미들웨어
- **Nginx**: L4 레벨 트래픽 제어

## 6. LLM 비용 최적화 전략

### 스마트 라우팅:
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

### 캐싱 전략:
- **Redis 캐싱**: 유사한 이력서에 대한 결과 재사용
- **임베딩 기반**: 이력서 유사도 측정 후 캐시 활용
- **TTL 관리**: 시간 기반 캐시 무효화

## 7. 응답 시간 기반 폴백 전략

### 지능형 폴백:
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

### 성능 지표:
- **P95 응답 시간**: 3초 이내 목표
- **모델별 SLA**: 개별 모델 성능 추적
- **자동 스케일링**: 트래픽 기반 인스턴스 조정

