"""
테스트 공통 설정 및 픽스처
"""
import pytest
import asyncio
import httpx
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient

# API 기본 URL
API_BASE_URL = "http://api.localhost/api/v1"

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """세션 스코프 이벤트 루프"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def http_client():
    """HTTP 클라이언트 픽스처"""
    async with httpx.AsyncClient(
        base_url=API_BASE_URL,
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
        "work_experiences": [
            {
                "company": "테스트회사",
                "position": "백엔드 개발자",
                "duration": "2022.01 ~ 현재",
                "project_name": "테스트 플랫폼 API 개발",
                "tech_stack": ["Java", "Spring Boot", "MySQL", "Redis", "AWS"],
                "achievements": [
                    "MSA 기반 시스템 설계 및 구현",
                    "Redis 캐싱으로 API 응답 속도 50% 개선"
                ]
            }
        ],
        "personal_projects": [
            {
                "name": "테스트 프로젝트",
                "description": "WebSocket 기반 실시간 서비스",
                "tech_stack": ["Spring Boot", "WebSocket", "PostgreSQL"],
                "key_achievements": [
                    "실시간 통신 시스템 구현",
                    "Docker 컨테이너화"
                ]
            }
        ],
        "technical_skills": {
            "programming_languages": ["Java", "Python"],
            "frameworks": ["Spring Boot", "FastAPI"],
            "databases": ["MySQL", "PostgreSQL", "Redis"],
            "cloud_platforms": ["AWS"],
            "devops_tools": ["Docker", "GitHub Actions"]
        },
        "total_experience_months": 36,
        "activities": [
            {
                "name": "테스트 활동",
                "type": "개발활동",
                "description": "오픈소스 기여"
            }
        ]
    }

@pytest.fixture
def existing_resume_keys():
    """기존에 생성된 이력서 키들"""
    return [
        "윤정은_1",
        "이민기_1", 
        "라이언_1"
    ]

@pytest.fixture
def test_providers():
    """테스트용 LLM 프로바이더 목록"""
    return ["gemini", "openai", "claude"]

# 플레이키 테스트 마커
pytest.mark.flaky = pytest.mark.flaky(reruns=3, reruns_delay=2)
