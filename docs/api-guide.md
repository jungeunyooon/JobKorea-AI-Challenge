# API 사용 가이드

> AI Challenge API의 엔드포인트별 상세 사용법

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
- **카테고리화**: 기술/경험/문제해결/인성 등으로 구분
- **난이도 설정**: 초급/중급/고급 난이도 자동 배정

### 3. 개인 맞춤형 학습 경로 생성
- **API 엔드포인트**: `POST /api/v1/learning/{unique_key}/learning-path`
- **생성 개수**: 5~8개의 구체적인 학습 경로
- **상세 정보**: 카테고리, 우선순위, 예상 기간, 추천 리소스 포함
- **실용성**: 구체적이고 실행 가능한 방안 제시

## API 엔드포인트

### Resume Service
- `POST /api/v1/resumes/` - 이력서 생성
- `GET /api/v1/resumes/{unique_key}` - 이력서 조회
- `GET /api/v1/resumes/` - 이력서 목록 조회
- `PUT /api/v1/resumes/{unique_key}` - 이력서 수정
- `DELETE /api/v1/resumes/{unique_key}` - 이력서 삭제

### Interview Service
- `POST /api/v1/interview/{unique_key}/questions` - 면접 질문 생성
- `GET /api/v1/interview/{unique_key}/questions` - 면접 질문 조회
- `GET /api/v1/interview/health` - 서비스 헬스체크

### Learning Service
- `POST /api/v1/learning/{unique_key}/learning-path` - 학습 경로 생성
- `GET /api/v1/learning/{unique_key}/learning-path` - 학습 경로 조회
- `GET /api/v1/learning/health` - 서비스 헬스체크

## 사용 예시

### 1. 이력서 생성
```bash
curl -X POST "http://api.localhost/api/v1/resumes/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김개발",
    "summary": "3년차 백엔드 개발자",
    "contact": {
      "email": "kim@example.com",
      "github": "https://github.com/kimdev"
    },
    "total_experience_months": 36
  }'
```

**응답:**
```json
{
  "message": "Resume created successfully",
  "resume_id": "507f1f77bcf86cd799439011",
  "unique_key": "김개발_1"
}
```

### 2. 면접 질문 생성
```bash
curl -X POST "http://api.localhost/api/v1/interview/김개발_1/questions"
```

**응답:**
```json
{
  "message": "Interview questions generated successfully",
  "unique_key": "김개발_1",
  "provider": "gemini",
  "model": "gemini-1.5-flash",
  "questions": [
    {
      "difficulty": "medium",
      "topic": "Spring Boot, MSA",
      "type": "Implementation",
      "question": "MSA 기반 주문/결제 시스템을 설계하실 때 서비스 간 데이터 일관성을 어떻게 보장하셨나요?"
    }
  ],
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### 3. 학습 경로 생성
```bash
curl -X POST "http://api.localhost/api/v1/learning/김개발_1/learning-path"
```

**응답:**
```json
{
  "message": "Learning path generated successfully",
  "unique_key": "김개발_1",
  "provider": "gemini",
  "model": "gemini-1.5-flash",
  "analysis": {
    "strengths": ["MSA 설계 경험", "성능 최적화 경험"],
    "weaknesses": ["클라우드 전문성 부족", "모니터링 경험 부족"]
  },
  "learning_paths": [
    {
      "type": "strength",
      "title": "MSA 아키텍처 심화",
      "description": "기존 MSA 경험을 바탕으로 고급 패턴 학습",
      "reason": "이미 MSA 구현 경험이 있으므로 전문성 강화",
      "resources": ["Event Sourcing", "CQRS", "Saga Pattern"],
      "link": "https://microservices.io/"
    }
  ],
  "generated_at": "2024-01-15T10:35:00Z"
}
```
 
## 개발 환경 설정

### 1. Hosts 파일 설정
```bash
# /etc/hosts에 추가
127.0.0.1 api.localhost
```

#### **서브도메인 설정**
- **API Gateway 주소**: `http://api.localhost`
- **Hosts 파일 설정 필요**: `/etc/hosts`에 `127.0.0.1 api.localhost` 추가
- api.localhost는 개발을 위한 설정이기 때문에 추후 도메인 연결이 필요합니다. 
- **서비스 접근**:
  - Resume API: http://api.localhost/api/v1/resumes/docs
  - Interview API: http://api.localhost/api/v1/interview/docs  
  - Learning API: http://api.localhost/api/v1/learning/docs
  - 통합 테스트 페이지: http://api.localhost/test
  - Traefik Dashboard: http://localhost:8080



### 2. 서비스 시작
```bash
docker compose up -d
```

### 3. API 문서 확인
- Resume API: http://api.localhost/api/v1/resumes/docs
- Interview API: http://api.localhost/api/v1/interview/docs  
- Learning API: http://api.localhost/api/v1/learning/docs
- Traefik Dashboard: http://localhost:8080
