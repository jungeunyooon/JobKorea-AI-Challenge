# Define common rules for project collaboration
_Exported on 2025. 8. 21. at 20시 56분 40초 GMT+9 from Cursor (1.4.5)_

---

**User**

난 프로젝트 하나를 만들건데 그 전에 .cursor/rules/rules.mdc를 사용해서 협업을 할때를 대비해서 미리 공통규칙을 정의할거야 
규칙 내용에는 내가 너한테 질문을 하면 너는 단계를 설명하고 나한테 승인을 받고 코드를 변경할 수 있다는 내용이 있어야해 

내가 만들 프로젝트의 주제는 다음과 같아 
구직자의 이력서 내용(경력, 직무, 기술 스킬)을 기반으로 생성형 AI가 맞춤형 면접 모의질문을 생성하고, 자기 개발 학습 경로를 제안하여 구직자의 합격률을 높이는 데 도움을 주는 백엔드 챗봇 API 설계 및 구현 합니다.
🎯 요구 기능
이력서 핵심 정보 입력
사용자로부터 경력 요약, 수행 직무, 보유 기술 스킬 리스트 등 이력서의 핵심 정보를 텍스트 형태로 입력 받는 API 구현해야 합니다. 
(예: "3년차 백엔드 개발자, Spring Boot/MSA/Python 기반 커머스 서비스 개발, AWS EC2 운영 경험")
참고 : 실제 이력서 파일 파싱 대신 핵심 정보를 직접 입력받는 방식으로 난이도 조절
생성형 AI 기반 맞춤 정보 제공
맞춤 면접 모의 질문 생성
입력된 경력, 직무, 기술 스킬에 기반하여 실제 면접에서 나올 법한 심충적인 질문 5개를 생성형 AI(LLM)가 생성하여 응답합니다.
자기 개발 및 합격률 향상 학습 경로 추천
입력된 정보를 분석하여, 구직자가 향후 개발 역량을 강화하고 합격률을 높일 수 있는 개인 맞춤형 합습 경로를 생성형 AI(LLM)가 제안합니다. 이 경로는 특정 기술 스택 심화, 관련 프로젝트 경험 쌓기, 커뮤니케이션 스킬 강화 등 구체적인 방안을 포함해야 합니다.

평가 기준은 다음과 같아 
생성형 AI 활용의 창의성 및 정교함
LLM 프롬프트 엔지니어링 전략이 얼마나 효과적이고 독창적인지
생성된 질문과 추천이 얼마나 '개인 맞춤형'의 특징을 잘 살렸는지
백엔드 아키텍처 및 구현
API 설계의 견고함 과 확장성
효율적인 데이터 처리 및 LLM 연동 방식
코드 가독성, 모듈성, 테스트 용이성 등 코드 품질
기능의 유용성 및 실용성
생성된 면접 질문이 실제 면접에 얼마나 도움이 되는지
제안된 학습 경로가 얼마나 구체적이고 현실적인 가이드가 되는지

이러한 것들도 고려해서 앞으로 방법들을 제시해야해 그럼 규칙 파일 만들어봐 규칙은 ai가 이해하기 쉽게 영어로 작성하고 

---

**Cursor**

프로젝트 구조를 이해했습니다. 구직자를 위한 맞춤형 면접 질문 생성 및 학습 경로 추천 백엔드 API를 개발하실 계획이군요. 먼저 협업을 위한 공통 규칙을 정의하겠습니다.

```markdown
# AI Collaboration Rules for Interview Preparation API Project

## Core Collaboration Process

### 1. Step-by-Step Approval Workflow
- When the user asks a question or requests changes, I must:
  1. **Explain the approach**: Break down the solution into clear, actionable steps
  2. **Wait for approval**: Get explicit confirmation before proceeding with code changes
  3. **Implement systematically**: Execute the approved plan step by step
  4. **Confirm completion**: Verify each step is completed before moving to the next

### 2. Communication Protocol
- Always provide a high-level overview before diving into implementation details
- Use clear, structured explanations with numbered steps
- Ask for clarification when requirements are ambiguous
- Summarize what was accomplished after each major change

## Project-Specific Guidelines

### 3. Interview Preparation API Development Rules

#### LLM Integration & Prompt Engineering
- Design prompts that generate personalized, realistic interview questions
- Ensure learning path recommendations are specific and actionable
- Implement proper error handling for LLM API failures
- Test prompt effectiveness with various input scenarios

#### API Design Principles
- Follow RESTful conventions for endpoint structure
- Implement comprehensive input validation for resume data
- Design scalable architecture for future feature expansion
- Include proper status codes and error responses

#### Data Processing Standards
- Structure resume input parsing for maximum flexibility
- Implement efficient caching for LLM responses when appropriate
- Design database schema for extensibility
- Ensure data privacy and security for user information

### 4. Code Quality Requirements

#### Architecture & Modularity
- Separate concerns: API layer, business logic, LLM integration, data layer
- Use dependency injection for testability
- Implement proper logging throughout the application
- Design for horizontal scaling

#### Testing Strategy
- Unit tests for business logic components
- Integration tests for LLM API interactions
- API endpoint testing with various input scenarios
- Mock LLM responses for consistent testing

#### Code Standards
- Use clear, descriptive naming conventions
- Include comprehensive docstrings/comments for complex logic
- Follow consistent code formatting
- Implement proper exception handling

### 5. Feature Development Process

#### Resume Analysis Features
- Validate input format and required fields
- Extract key information (experience, skills, role) systematically
- Handle edge cases (career gaps, multiple roles, diverse skill sets)

#### Interview Question Generation
- Generate 5 relevant, challenging questions per request
- Ensure questions are role-appropriate and experience-level matched
- Include both technical and behavioral question types
- Avoid generic or overly broad questions

#### Learning Path Recommendations
- Provide specific, actionable development steps
- Include technology stack improvements, project suggestions, and soft skills
- Make recommendations realistic and time-bound
- Consider current market trends and job requirements

## Implementation Workflow

### 6. Before Starting Any Development
1. Confirm understanding of the specific feature or requirement
2. Outline the implementation approach with clear steps
3. Identify potential challenges or dependencies
4. Get user approval before proceeding

### 7. During Development
- Provide progress updates for complex implementations
- Ask for feedback if implementation diverges from the plan
- Test functionality before marking tasks complete
- Document any assumptions or design decisions

### 8. After Implementation
- Demonstrate the working feature with examples
- Explain how the implementation meets the requirements
- Suggest potential improvements or next steps
- Update documentation as needed

## Quality Assurance

### 9. Definition of Done
- Code is functional and tested
- API endpoints respond correctly to valid/invalid inputs
- LLM integration produces relevant, high-quality outputs
- Error handling is comprehensive
- Code follows project standards and is well-documented

### 10. Continuous Improvement
- Regularly review and refine LLM prompts based on output quality
- Monitor API performance and optimize as needed
- Gather feedback on generated questions and recommendations
- Update rules and processes based on development experience

---

**Remember**: Always explain your approach and get approval before implementing changes. This ensures we build exactly what's needed while maintaining high code quality and project coherence.
```

완료되었습니다! `.cursor/rules/rules.mdc` 파일을 생성하여 협업 규칙을 정의했습니다.

## 주요 규칙 내용:

### 🤝 **핵심 협업 프로세스**
- **단계별 승인 워크플로우**: 질문을 받으면 → 접근 방법 설명 → 승인 대기 → 체계적 구현 → 완료 확인
- 명확한 구조화된 설명과 번호가 매겨진 단계로 소통

### 🎯 **프로젝트 특화 가이드라인**
- **LLM 통합 & 프롬프트 엔지니어링**: 개인 맞춤형 면접 질문 생성을 위한 효과적인 프롬프트 설계
- **API 설계 원칙**: RESTful 설계, 확장 가능한 아키텍처, 포괄적인 입력 검증
- **데이터 처리 표준**: 이력서 데이터 파싱, 효율적인 캐싱, 보안 고려사항

### 💻 **코드 품질 요구사항**
- 모듈화된 아키텍처 (API 계층, 비즈니스 로직, LLM 통합, 데이터 계층 분리)
- 포괄적인 테스팅 전략 (단위/통합/API 테스트)
- 명확한 명명 규칙과 문서화

### 🚀 **기능 개발 프로세스**
- **면접 질문 생성**: 역할에 적합하고 경험 수준에 맞는 5개의 관련성 높은 질문
- **학습 경로 추천**: 구체적이고 실행 가능한 개발 단계, 시장 트렌드 반영

이제부터 이 규칙에 따라 협업하겠습니다. 앞으로 어떤 요청을 하시든 먼저 **접근 방법을 설명하고 승인을 받은 후** 코드 변경을 진행하겠습니다.

다음 단계로 무엇을 진행하시겠습니까? 프로젝트 초기 설정이나 특정 기능 구현을 시작하시겠습니까?

---

**User**

Best practices
Good rules are focused, actionable, and scoped.
Keep rules under 500 lines
Split large rules into multiple, composable rules
Provide concrete examples or referenced files
Avoid vague guidance. Write rules like clear internal docs
Reuse rules when repeating prompts in chat
​
@https://docs.cursor.com/en/context/rules 
지금 파일은 너무 길어
공식문서에 따르면 규칙은 500줄 이하를 권장하고 있어 너가 작성한 파일을 여러 규칙으로 나눠

---

**Cursor**

맞습니다! [Cursor 공식문서](https://docs.cursor.com/en/context/rules)에 따르면 규칙은 500줄 이하로 유지하고 여러 개의 조합 가능한 규칙으로 나누는 것이 좋습니다.

## 🔄 **현재 규칙 파일 분할 계획**

현재 작성한 긴 규칙 파일을 다음과 같이 **5개의 집중된 규칙**으로 나누겠습니다:

### 1. **collaboration.mdc** (Always Apply)
- 핵심 협업 프로세스 (승인 워크플로우)
- 커뮤니케이션 프로토콜
- 구현 워크플로우

### 2. **architecture.mdc** (Auto Attached - backend/*)
- 아키텍처 및 모듈성 요구사항
- 코드 표준 및 품질
- 의존성 주입 및 확장성

### 3. **llm-integration.mdc** (Auto Attached - *llm*, *ai*, *prompt*)
- LLM 통합 및 프롬프트 엔지니어링
- AI 응답 처리 및 오류 핸들링
- 캐싱 전략

### 4. **api-development.mdc** (Auto Attached - *api*, *controller*, *route*)
- RESTful API 설계 원칙
- 이력서 분석 및 면접 질문 생성 기능
- 학습 경로 추천 로직

### 5. **testing-qa.mdc** (Auto Attached - *test*, *spec*)
- 테스팅 전략 (단위/통합/API 테스트)
- 품질 보증 및 Definition of Done
- 지속적 개선

각 규칙은 관련 파일 패턴에 따라 자동으로 적용되고, 구체적인 예시와 참조 파일을 포함할 예정입니다.

**이 분할 계획으로 진행해도 되겠습니까?** 승인해주시면 기존 파일을 삭제하고 새로운 규칙들을 생성하겠습니다.

---

**User**

그렇게 해

---

**Cursor**

승인 받았습니다! 기존 파일을 삭제하고 5개의 집중된 규칙으로 분할하겠습니다.

```markdown
---
description: Core collaboration workflow and approval process
alwaysApply: true
---

# Core Collaboration Process

## Step-by-Step Approval Workflow
When the user asks a question or requests changes, I must:
1. **Explain the approach**: Break down the solution into clear, actionable steps
2. **Wait for approval**: Get explicit confirmation before proceeding with code changes
3. **Implement systematically**: Execute the approved plan step by step
4. **Confirm completion**: Verify each step is completed before moving to the next

## Communication Protocol
- Always provide a high-level overview before diving into implementation details
- Use clear, structured explanations with numbered steps
- Ask for clarification when requirements are ambiguous
- Summarize what was accomplished after each major change

## Implementation Workflow

### Before Starting Any Development
1. Confirm understanding of the specific feature or requirement
2. Outline the implementation approach with clear steps
3. Identify potential challenges or dependencies
4. Get user approval before proceeding

### During Development
- Provide progress updates for complex implementations
- Ask for feedback if implementation diverges from the plan
- Test functionality before marking tasks complete
- Document any assumptions or design decisions

### After Implementation
- Demonstrate the working feature with examples
- Explain how the implementation meets the requirements
- Suggest potential improvements or next steps
- Update documentation as needed

---

**Remember**: Always explain your approach and get approval before implementing changes.
```

```markdown
---
description: Architecture and code quality standards for backend development
globs: ["**/backend/**", "**/src/**", "**/app/**", "**/server/**"]
alwaysApply: false
---

# Architecture & Code Quality

## Modularity Requirements
- Separate concerns: API layer, business logic, LLM integration, data layer
- Use dependency injection for testability
- Implement proper logging throughout the application
- Design for horizontal scaling

## Code Standards
- Use clear, descriptive naming conventions
- Include comprehensive docstrings/comments for complex logic
- Follow consistent code formatting
- Implement proper exception handling

## Data Processing Standards
- Structure resume input parsing for maximum flexibility
- Implement efficient caching for LLM responses when appropriate
- Design database schema for extensibility
- Ensure data privacy and security for user information

## Architecture Principles
- Follow SOLID principles for maintainable code
- Implement clean architecture patterns
- Use environment-based configuration
- Design stateless services for scalability

## Error Handling
- Implement comprehensive error handling at all layers
- Use structured logging for debugging
- Return meaningful error messages to clients
- Implement circuit breaker patterns for external service calls
```

```markdown
---
description: LLM integration and prompt engineering guidelines
globs: ["**/*llm*", "**/*ai*", "**/*prompt*", "**/*openai*", "**/*chat*"]
alwaysApply: false
---

# LLM Integration & Prompt Engineering

## Prompt Design Principles
- Design prompts that generate personalized, realistic interview questions
- Ensure learning path recommendations are specific and actionable
- Include role-appropriate context and experience level matching
- Test prompt effectiveness with various input scenarios

## Interview Question Generation
- Generate exactly 5 relevant, challenging questions per request
- Include both technical and behavioral question types
- Avoid generic or overly broad questions
- Ensure questions match the candidate's experience level and target role

## Learning Path Recommendations
- Provide specific, actionable development steps
- Include technology stack improvements, project suggestions, and soft skills
- Make recommendations realistic and time-bound
- Consider current market trends and job requirements

## Error Handling & Reliability
- Implement proper error handling for LLM API failures
- Add retry logic with exponential backoff
- Implement fallback responses for service unavailability
- Log all LLM interactions for debugging and improvement

## Performance Optimization
- Implement efficient caching for repeated queries
- Use streaming responses when appropriate
- Optimize token usage for cost efficiency
- Monitor response times and quality metrics
```

```markdown
---
description: RESTful API design and development standards
globs: ["**/*api*", "**/*controller*", "**/*route*", "**/*endpoint*", "**/*handler*"]
alwaysApply: false
---

# API Development Standards

## RESTful Design Principles
- Follow RESTful conventions for endpoint structure
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Implement proper status codes and error responses
- Design scalable architecture for future feature expansion

## Input Validation
- Implement comprehensive input validation for resume data
- Validate all required fields before processing
- Sanitize inputs to prevent security vulnerabilities
- Return clear validation error messages

## Resume Analysis Features
- Accept core resume information: experience summary, role, skills list
- Validate input format and required fields
- Extract key information systematically
- Handle edge cases (career gaps, multiple roles, diverse skill sets)

## Response Design
- Return consistent JSON response formats
- Include proper error codes and messages
- Implement pagination for large result sets
- Add response metadata (timestamps, request IDs)

## Security & Performance
- Implement rate limiting for API endpoints
- Add authentication/authorization as needed
- Use HTTPS for all communications
- Implement request/response logging
- Add response compression for large payloads

## Example Endpoints
```
POST /api/resume/analyze
POST /api/interview/questions
POST /api/learning/path
GET /api/health
```
```

```markdown
---
description: Testing strategy and quality assurance guidelines
globs: ["**/*test*", "**/*spec*", "**/test/**", "**/tests/**"]
alwaysApply: false
---

# Testing & Quality Assurance

## Testing Strategy
- Unit tests for business logic components
- Integration tests for LLM API interactions
- API endpoint testing with various input scenarios
- Mock LLM responses for consistent testing

## Test Coverage Requirements
- Minimum 80% code coverage for business logic
- Test both happy path and error scenarios
- Include edge case testing for resume parsing
- Test LLM integration with mock responses

## Quality Assurance Standards

### Definition of Done
- Code is functional and tested
- API endpoints respond correctly to valid/invalid inputs
- LLM integration produces relevant, high-quality outputs
- Error handling is comprehensive
- Code follows project standards and is well-documented

### Testing Best Practices
- Write tests before implementing features (TDD approach)
- Use descriptive test names that explain the scenario
- Keep tests isolated and independent
- Use appropriate test doubles (mocks, stubs, fakes)

## Continuous Improvement
- Regularly review and refine LLM prompts based on output quality
- Monitor API performance and optimize as needed
- Gather feedback on generated questions and recommendations
- Update tests when requirements change

## Performance Testing
- Load testing for API endpoints
- Response time monitoring
- Memory usage profiling
- LLM API latency tracking
```

✅ **완료되었습니다!** 긴 규칙 파일을 [Cursor 공식문서](https://docs.cursor.com/en/context/rules)의 모범 사례에 따라 **5개의 집중된 규칙**으로 분할했습니다.

## 📋 **새로운 규칙 구조**

### 1. **🤝 collaboration.mdc** (Always Apply)
- **항상 적용**: 모든 상황에서 활성화
- 핵심 승인 워크플로우 및 커뮤니케이션 프로토콜
- 단계별 접근 방법 설명 → 승인 대기 → 구현 프로세스

### 2. **🏗️ architecture.mdc** (Auto Attached)
- **자동 적용**: `backend/`, `src/`, `app/`, `server/` 디렉토리 파일 작업 시
- 아키텍처 설계 원칙, 모듈성, 코드 품질 표준
- 의존성 주입, 로깅, 확장성 고려사항

### 3. **🤖 llm-integration.mdc** (Auto Attached)
- **자동 적용**: LLM, AI, prompt 관련 파일 작업 시
- 프롬프트 엔지니어링 전략, 면접 질문 생성 규칙
- 학습 경로 추천, 오류 처리, 성능 최적화

### 4. **🌐 api-development.mdc** (Auto Attached)
- **자동 적용**: API, controller, route, endpoint 파일 작업 시
- RESTful 설계 원칙, 입력 검증, 보안
- 이력서 분석 기능, 응답 형식 표준화

### 5. **🧪 testing-qa.mdc** (Auto Attached)
- **자동 적용**: 테스트 파일 작업 시
- 테스팅 전략, 품질 보증 기준
- Definition of Done, 지속적 개선 프로세스

## 🎯 **규칙 적용 방식**
- **collaboration.mdc**: 모든 대화에서 항상 활성화
- **나머지 4개**: 관련 파일 패턴과 일치하는 파일 작업 시 자동으로 활성화
- 각 규칙은 500줄 이하로 유지되어 [공식 모범 사례](https://docs.cursor.com/en/context/rules)를 준수

이제 프로젝트 개발을 시작할 준비가 되었습니다! 다음 단계로 무엇을 진행하시겠습니까?

---

**User**

 collaboration.mdc 이것만 유지하고 나머지는 개발하면서 고민해보는게 좋을것같아 너는 ai가 내가 만드는게 어떤 프로젝트인지 이해할 수 있는 규칙도 추가하는게 좋을까? 어떻게 생각해?

---

**Cursor**

정말 좋은 판단입니다! 나머지 규칙들을 삭제하고 `collaboration.mdc`만 유지하는 것이 현명한 접근입니다.

## 🤔 **프로젝트 컨텍스트 규칙 추가에 대한 의견**

**추가하는 것을 강력히 추천합니다!** 이유는:

### ✅ **프로젝트 컨텍스트 규칙의 장점**
1. **일관된 개발 방향**: AI가 항상 프로젝트 목적을 기억하고 관련 제안을 할 수 있음
2. **요구사항 준수**: 핵심 기능(면접 질문 생성, 학습 경로 추천)을 항상 고려
3. **평가 기준 인식**: 창의성, 아키텍처, 실용성 기준을 염두에 둔 개발
4. **컨텍스트 유지**: 긴 대화에서도 프로젝트 목표를 잃지 않음

### 📋 **추가할 내용 제안**
```mdc
# Project Context: Interview Preparation API

## Project Overview
구직자의 이력서 내용을 기반으로 맞춤형 면접 질문과 학습 경로를 제공하는 백엔드 API

## Core Features
- 이력서 핵심 정보 입력 API
- LLM 기반 맞춤 면접 질문 5개 생성
- 개인화된 자기개발 학습 경로 추천

## Evaluation Criteria
- 생성형 AI 활용의 창의성 및 정교함
- 백엔드 아키텍처의 견고함과 확장성
- 실제 도움이 되는 실용성
```

**이렇게 간단한 프로젝트 컨텍스트 규칙을 `collaboration.mdc`에 추가하거나 별도 파일로 만드는 것이 좋겠습니다.**

어떤 방식을 선호하시나요?
1. `collaboration.mdc`에 프로젝트 컨텍스트 섹션 추가
2. 별도의 `project-context.mdc` 파일 생성

```plaintext
# Project Context: Interview Preparation API

## Project Overview
구직자의 이력서 내용을 기반으로 맞춤형 면접 질문과 학습 경로를 제공하는 백엔드 API

## Core Features
- 이력서 핵심 정보 입력 API
- LLM 기반 맞춤 면접 질문 5개 생성
- 개인화된 자기개발 학습 경로 추천

## Evaluation Criteria
- 생성형 AI 활용의 창의성 및 정교함
- 백엔드 아키텍처의 견고함과 확장성
- 실제 도움이 되는 실용성
```

---

**User**

별도의 project-context.mdc 파일 생성하도록 해

---

**Cursor**

승인 받았습니다! 별도의 `project-context.mdc` 파일을 생성하겠습니다.

```markdown
---
description: Project context and core requirements for Interview Preparation API
alwaysApply: true
---

# Project Context: Interview Preparation API

## Project Overview
구직자의 이력서 내용(경력, 직무, 기술 스킬)을 기반으로 생성형 AI가 맞춤형 면접 모의질문을 생성하고, 자기 개발 학습 경로를 제안하여 구직자의 합격률을 높이는 데 도움을 주는 백엔드 챗봇 API

## Core Features

### 1. 이력서 핵심 정보 입력
- 경력 요약, 수행 직무, 보유 기술 스킬 리스트 등 핵심 정보를 텍스트 형태로 입력받는 API
- 예시: "3년차 백엔드 개발자, Spring Boot/MSA/Python 기반 커머스 서비스 개발, AWS EC2 운영 경험"
- 실제 이력서 파일 파싱 대신 핵심 정보를 직접 입력받는 방식

### 2. 맞춤 면접 모의 질문 생성
- 입력된 경력, 직무, 기술 스킬에 기반하여 실제 면접에서 나올 법한 심층적인 질문 **5개**를 LLM이 생성
- 개인 맞춤형 특징을 살린 질문 생성

### 3. 자기 개발 학습 경로 추천
- 구직자가 향후 개발 역량을 강화하고 합격률을 높일 수 있는 개인 맞춤형 학습 경로 제안
- 특정 기술 스택 심화, 관련 프로젝트 경험 쌓기, 커뮤니케이션 스킬 강화 등 구체적인 방안 포함

## Evaluation Criteria

### 1. 생성형 AI 활용의 창의성 및 정교함
- LLM 프롬프트 엔지니어링 전략이 얼마나 효과적이고 독창적인지
- 생성된 질문과 추천이 얼마나 '개인 맞춤형'의 특징을 잘 살렸는지

### 2. 백엔드 아키텍처 및 구현
- API 설계의 견고함과 확장성
- 효율적인 데이터 처리 및 LLM 연동 방식
- 코드 가독성, 모듈성, 테스트 용이성 등 코드 품질

### 3. 기능의 유용성 및 실용성
- 생성된 면접 질문이 실제 면접에 얼마나 도움이 되는지
- 제안된 학습 경로가 얼마나 구체적이고 현실적인 가이드가 되는지

## Development Focus
- 창의적이고 효과적인 프롬프트 엔지니어링
- 견고하고 확장 가능한 백엔드 아키텍처
- 실제로 도움이 되는 실용적인 기능 구현
```

✅ **완료되었습니다!** `project-context.mdc` 파일을 생성했습니다.

## 📋 **현재 활성화된 규칙 구조**

### 🤝 **collaboration.mdc** (Always Apply)
- 핵심 승인 워크플로우 및 커뮤니케이션 프로토콜

### 🎯 **project-context.mdc** (Always Apply)
- **프로젝트 개요**: 구직자 맞춤형 면접 준비 API
- **핵심 기능 3가지**:
  - 이력서 핵심 정보 입력 API
  - LLM 기반 맞춤 면접 질문 5개 생성
  - 개인화된 학습 경로 추천
- **평가 기준**: AI 창의성, 백엔드 아키텍처, 실용성
- **개발 포커스**: 프롬프트 엔지니어링, 견고한 아키텍처, 실용적 기능

이제 AI가 항상 프로젝트의 목적과 요구사항을 기억하면서 협업할 수 있습니다. 개발 과정에서 필요한 추가 규칙들은 실제 구현하면서 점진적으로 만들어나가면 됩니다.

다음 단계로 **프로젝트 초기 설정**을 시작하시겠습니까? 
- 프로젝트 구조 설계
- 기술 스택 선택 
- 개발 환경 설정
- 또는 다른 우선순위가 있으시다면?

---
