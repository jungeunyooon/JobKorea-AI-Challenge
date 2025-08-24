# AI 협업 가이드

> AI Challenge 프로젝트에서 Claude, GitHub Copilot, Cursor IDE와 효과적으로 협업하는 방법

## AI 설정 파일 구조
```
AI-Challenge/
├── .claude/
│   └── setting.json          # Claude AI 컨텍스트 설정
├── .cursor/
│   └── rules/
│       ├── fastapi-clean-code.md     # 코딩 규칙
│       └── project-guidelines.md     # 프로젝트 가이드라인
├── copilot-instructions.md   # GitHub Copilot 가이드라인
└── AI-COLLABORATION.md       # 이 파일
```

## 각 AI 도구별 역할

### Claude AI - 아키텍처 설계 & 코드 리뷰
**최적 활용 시나리오:**
- 복잡한 비즈니스 로직 설계
- 코드 리팩토링 전략 수립
- 아키텍처 의사결정 지원
- 깊이 있는 코드 리뷰

**설정 파일:** `.claude/setting.json`

**대화 예시:**
```
"현재 LLM 통합 아키텍처에서 폴백 전략을 개선하고 싶습니다. 
Gemini → OpenAI → Claude 순서로 폴백하는데, 
각 provider별 특성을 고려한 더 지능적인 라우팅 전략을 제안해주세요."
```

### GitHub Copilot - 실시간 코드 생성
**최적 활용 시나리오:**
- 반복적인 CRUD 코드 생성
- 테스트 케이스 자동 생성
- 유틸리티 함수 구현
- 보일러플레이트 코드 작성

**설정 파일:** `copilot-instructions.md`

**프롬프트 예시:**
```python
# Create FastAPI endpoint for learning path generation with:
# - Input: unique_key (path param)
# - Output: LearningPathResponse model
# - Error handling: 404 for invalid resume
# - LLM integration with fallback strategy
```

### Cursor IDE - 컨텍스트 기반 편집
- [Cursor Rules Guide](https://github.com/PatrickJS/awesome-cursorrule) 를 참고하여 만들었습니다.

**최적 활용 시나리오:**
- 파일 간 일관성 유지
- 프로젝트 전체 리팩토링
- 의존성 추적 및 수정
- 컨텍스트 기반 버그 수정

**설정 파일:** `.cursor/rules/`

## AI 협업 워크플로우

### 1. 기획 단계 (Claude)
```
요구사항 분석
↓
아키텍처 설계
↓  
기술 스펙 문서화
```

### 2. 개발 단계 (Copilot + Cursor)
```
Copilot: 코드 스켈레톤 생성
↓
Cursor: 컨텍스트 기반 완성
↓
Copilot: 테스트 코드 생성
```

### 3. 검토 단계 (Claude)
```
코드 리뷰 요청
↓
성능 분석
↓
개선 제안
```


## 실전 활용 팁

### Claude와의 효과적인 대화법
```markdown
Good:
"현재 interview_service.py의 generate_questions 함수에서 
LLM API 호출 실패 시 재시도 로직을 구현하고 싶습니다.
현재 코드 구조와 에러 처리 패턴을 고려해서 
어떤 방식이 가장 적절할까요?"

Avoid:
"코드 좀 고쳐줘"
```

### Copilot 프롬프트 최적화
```python
# 구체적인 요구사항을 주석으로 명시
# "Generate async function to validate resume data with:
# - Input: dict (resume data from MongoDB)
# - Output: ValidationResult (custom Pydantic model)  
# - Validation: required fields, data types, business rules
# - Error handling: raise ValidationError with detailed message"

async def validate_resume_data(resume_data: dict) -> ValidationResult:
    # Copilot이 여기서 구현...
```

### Cursor 컨텍스트 활용
```
1. 관련 파일들을 모두 열어두기
2. @filename 으로 특정 파일 참조
3. 전체 프로젝트 구조 인식 활용
4. 일관된 네이밍 패턴 유지
```

## 학습 리소스

### AI 프롬프트 엔지니어링
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Claude Best Practices](https://docs.anthropic.com/claude/docs)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)

### FastAPI + AI 개발
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Python Type Hints Guide](https://docs.python.org/3/library/typing.html)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)

---

