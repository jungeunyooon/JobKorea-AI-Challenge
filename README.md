# AI Challenge: 이력서 기반 맞춤형 커리어 코치 챗봇 API

## 프로젝트 개요

구직자의 이력서를 분석하여 개인 맞춤형 면접 질문과 학습 경로를 제공하는 AI 기반 백엔드 서비스입니다.  
아래 문서에서 더 자세한 내용을 확인할 수 있습니다.

## 문서 링크

- [아키텍처 상세](./docs/architecture.md)
- [API 사용법](./docs/api-guide.md)
- [LLM 통합](./docs/llm-integration.md)
- [테스트 전략](./docs/testing.md)
- [프롬프팅 전략](./docs/prompting-strategy.md)
- [AI 협업](./docs/ai-collaboration.md)
- [향후 계획](./docs/future-plans.md)

## 시작 방법

```bash
# 1. Git clone
git clone https://github.com/jungeunyooon/AI-Challenge.git

# 2. 서비스 실행
docker-compose up -d

# 3. API 확인
curl http://api.localhost/api/v1/resumes/health
```

## 환경 변수

`.env` 파일에 다음 환경변수들을 설정해야 합니다:

- **MongoDB**: `MONGODB_URL`, `DATABASE_NAME`, `MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD`
- **OpenAI**: `OPENAI_API_KEY` 등 OpenAI 관련 설정
- **Claude**: `CLAUDE_API_KEY` 등 Claude 관련 설정  
- **Gemini**: `GEMINI_API_KEY` 등 Gemini 관련 설정

자세한 설정은 [`env.example`](./env.example) 파일을 참고하세요. 