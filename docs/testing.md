# 테스트 전략

> AI Challenge API의 종합적인 테스트 전략 및 구현

## 테스트 전략 개요

### **Given-When-Then 패턴 (BDD)**

<details>
<summary>BDD 테스트 예시</summary>

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

### **Table Driven Test**
다양한 시나리오를 효율적으로 테스트:

<details>
<summary>파라미터화된 테스트 예시</summary>

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

### **Flaky Test 대응 전략**

<details>
<summary>Flaky Test 대응 전략</summary>

#### **자동 재실행 (Rerun)**
```python
# pytest-rerunfailures 사용
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_llm_api_call():
    """LLM API 호출 테스트 - 네트워크 이슈로 인한 실패 시 재시도"""
    response = client.post("/interview/test_user/questions")
    assert response.status_code == 200
    assert response.json()["provider"] in ["gemini", "openai", "claude"]  # 폴백 허용
```

#### **병렬 실행 (Parallel)**
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

#### **Timeout 및 Retry 로직**
```python
@pytest.mark.timeout(30)  # 30초 타임아웃
@pytest.mark.retry(max_attempts=3, backoff=1.5)
def test_learning_path_generation():
    """학습 경로 생성 테스트 - 타임아웃 및 재시도"""
    response = client.post("/learning/test_user/learning-path")
    assert response.status_code == 200
```

</details>

### **Celery 파이프라인 테스트**

<details>
<summary>Celery 파이프라인 테스트 예시</summary>

#### **기본 설정 및 픽스처**
```python
@pytest.fixture
def mock_celery_task():
    with patch('celery.Task') as mock:
        mock.return_value.delay.return_value = AsyncResult('test-id')
        yield mock

@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        mock.return_value.get.return_value = b'{"status": "completed"}'
        yield mock

@pytest.fixture
def mock_rabbitmq():
    with patch('kombu.Connection') as mock:
        yield mock
```

#### **면접 질문 생성 파이프라인**
```python
@pytest.mark.asyncio
async def test_interview_pipeline(mock_celery_task, mock_redis):
    """면접 질문 생성 파이프라인 테스트"""
    # Given: 이력서 데이터가 주어지고
    resume_data = {
        "name": "테스트개발자",
        "technical_skills": ["Python", "FastAPI"]
    }
    
    # When: 태스크를 실행하면
    result = generate_interview_questions.delay(resume_data)
    
    # Then: 태스크가 큐에 들어가고 결과가 저장된다
    assert result.id == 'test-id'
    stored_result = mock_redis.return_value.get(
        f'interview:result:{result.id}'
    )
    assert stored_result is not None
```

#### **태스크 체인 테스트**
```python
def test_chain_tasks(mock_celery_task):
    """태스크 체인 테스트"""
    # Given: 태스크 체인이 구성되고
    task_chain = chain(
        preprocess_resume.s({"name": "테스트"}),
        generate_interview_questions.s(),
        post_process_questions.s()
    )
    
    # When: 체인을 실행하면
    result = task_chain.delay()
    
    # Then: 모든 태스크가 순차적으로 실행된다
    assert result.id == 'test-id'
    task = mock_celery_task.return_value
    assert task.delay.call_count == 3
```

#### **태스크 진행 상황 추적**
```python
def test_task_progress_tracking(mock_redis):
    """태스크 진행 상황 추적 테스트"""
    # Given: 태스크 ID가 주어지고
    task_id = 'test-progress-id'
    
    # When: 진행 상황을 업데이트하면
    progress_data = {
        "status": "in_progress",
        "current_step": 2,
        "total_steps": 5,
        "message": "면접 질문 생성 중..."
    }
    mock_redis.return_value.set(
        f'task:progress:{task_id}',
        str(progress_data)
    )
    
    # Then: Redis에 진행 상황이 저장된다
    stored_progress = mock_redis.return_value.get(
        f'task:progress:{task_id}'
    )
    assert stored_progress is not None
```

#### **에러 처리 및 재시도**
```python
@pytest.mark.asyncio
async def test_error_handling(mock_celery_task, mock_redis):
    """에러 처리 및 복구 테스트"""
    # Given: 태스크가 실패하도록 설정
    mock_celery_task.return_value.delay.side_effect = \
        Exception("LLM API 오류")
    
    # When & Then: 에러가 발생하면 적절히 처리된다
    with pytest.raises(Exception):
        result = mock_celery_task.return_value.delay({"test": "data"})
        error_data = mock_redis.return_value.get(
            f'task:error:{result.id}'
        )
        assert b"LLM API 오류" in error_data
```

</details>

## 테스트 구조

### 디렉토리 구조
```
backend/tests/
├── conftest.py                    # 공통 설정 및 픽스처
├── pytest.ini                    # pytest 설정
├── unit/
│   ├── test_basic_utils.py       # 기본 유틸리티 
│   ├── test_utils.py             # 고급 유틸리티
│   └── test_celery_tasks.py      # Celery 태스크 테스트
├── interview-service/
│   ├── test_interview_bdd.py     # BDD 패턴 테스트
│   ├── test_interview_table_driven.py  # Table Driven 테스트
│   └── test_interview_flaky.py   # Flaky Test 대응
├── learning-service/
│   └── test_learning_path_bdd.py # 장점/단점 분석 테스트
└── resume-service/
    └── test_resume_crud.py       # CRUD 기능 테스트
```

### 테스트 픽스처 (conftest.py)
```python
@pytest.fixture
async def http_client():
    """HTTP 클라이언트 픽스처"""
    async with httpx.AsyncClient(
        base_url="http://api.localhost/api/v1",
        timeout=30.0,
        follow_redirects=True
    ) as client:
        yield client

@pytest.fixture
def test_resume_data():
    """테스트용 이력서 데이터"""
    return {
        "name": "테스트개발자",
        "summary": "3년차 백엔드 개발자로 Spring Boot 기반 마이크로서비스 개발 경험",
        "contact": {
            "email": "test.dev@example.com",
            "github": "https://github.com/testdev",
            "phone": "010-1234-5678"
        },
        "technical_skills": {
            "programming_languages": ["Java", "Python"],
            "frameworks": ["Spring Boot", "FastAPI"],
            "databases": ["MySQL", "PostgreSQL", "Redis"],
            "cloud_platforms": ["AWS"],
            "devops_tools": ["Docker", "GitHub Actions"]
        },
        "total_experience_months": 36
    }
```

## 테스트 실행 가이드

### 기본 테스트 실행
```bash
# 전체 테스트 실행
make test

# 서비스별 테스트
make test-interview
make test-learning  
make test-resume

# 패턴별 테스트
make test-bdd           # Given-When-Then
make test-flaky         # Flaky 테스트
make test-parallel      # 병렬 실행
make test-celery        # Celery 파이프라인 테스트

# 유닛 테스트 (API 서버 불필요)
pytest tests/unit/ -v
```

### 고급 테스트 실행
```bash
# 커버리지 포함 실행
make test-coverage

# 병렬 실행 (4개 워커)
make test-parallel-4

# 느린 테스트 제외
make test-fast

# 실패한 테스트만 재실행
make test-failed

# 디버그 모드
make test-debug
```

## 테스트 카테고리

### 1. 유닛 테스트 (Unit Tests)
```python
# 외부 의존성 없는 순수 함수 테스트
def test_remove_markdown_from_json():
    """JSON에서 마크다운 제거 유틸리티 테스트"""
    markdown_json = '''```json
    {"test": "value", "number": 123}
    ```'''
    
    result = remove_markdown_from_json(markdown_json)
    assert result == '{"test": "value", "number": 123}'
```

### 2. 통합 테스트 (Integration Tests)
```python
# API 엔드포인트와 데이터베이스 통합 테스트
@pytest.mark.integration
async def test_end_to_end_interview_flow(http_client):
    """이력서 생성 → 면접 질문 생성 전체 플로우"""
    # 1. 이력서 생성
    resume_response = await http_client.post("/resumes/", json=test_resume)
    unique_key = resume_response.json()["unique_key"]
    
    # 2. 면접 질문 생성
    questions_response = await http_client.post(f"/interview/{unique_key}/questions")
    assert questions_response.status_code == 200
```

### 3. 성능 테스트 (Performance Tests)
```python
@pytest.mark.performance
async def test_response_time_performance(http_client):
    """응답 시간 성능 테스트"""
    import time
    
    start_time = time.time()
    response = await http_client.post("/interview/윤정은_1/questions")
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response.status_code == 200
    assert response_time < 10, f"Response took {response_time:.2f}s"
```

## Mock 및 Stub 전략

### LLM API 모킹
```python
@pytest.fixture
def mock_llm_response():
    return {
        "questions": [
            {
                "difficulty": "medium",
                "topic": "Spring Boot, MSA",
                "type": "Implementation",
                "question": "MSA 아키텍처에서 서비스 간 통신 방법은?"
            }
        ]
    }

@patch('shared.llm.registry.get_llm_client')
async def test_with_mock_llm(mock_client, mock_llm_response):
    mock_client.return_value.ainvoke.return_value.content = json.dumps(mock_llm_response)
    
    response = await client.post("/interview/test_user/questions")
    assert response.status_code == 200
```

### 데이터베이스 모킹
```python
@patch('motor.motor_asyncio.AsyncIOMotorClient')
async def test_with_mock_db(mock_mongo):
    mock_db = mock_mongo.return_value.ai_challenge
    mock_db.resumes.find_one.return_value = {"name": "test"}
    
    # 테스트 로직...
```

## 테스트 데이터 관리

### 테스트 데이터 세트
```python
# tests/fixtures/resume_samples.py
SAMPLE_RESUMES = {
    "junior_developer": {
        "name": "신입개발자",
        "total_experience_months": 6,
        "technical_skills": ["Python", "Flask"]
    },
    "senior_developer": {
        "name": "시니어개발자", 
        "total_experience_months": 60,
        "technical_skills": ["Java", "Spring", "Kubernetes"]
    },
    "fullstack_developer": {
        "name": "풀스택개발자",
        "total_experience_months": 36,
        "technical_skills": ["React", "Node.js", "PostgreSQL"]
    }
}
```

### 테스트 환경 분리
```python
# 테스트용 환경 설정
@pytest.fixture(scope="session")
def test_settings():
    return Settings(
        mongodb_url="mongodb://localhost:27017/test_ai_challenge",
        openai_api_key="test-key",
        log_level="DEBUG"
    )
```

### 테스트 리포트
```bash
# HTML 커버리지 리포트 생성
make test-coverage
open htmlcov/index.html

# JUnit XML 리포트
pytest --junit-xml=test-results.xml

# 성능 벤치마크
pytest --benchmark-only
```