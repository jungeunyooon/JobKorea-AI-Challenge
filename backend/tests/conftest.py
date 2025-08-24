"""
테스트 공통 설정 및 픽스처
"""
import pytest
import asyncio
import httpx
import os
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv
from tests.test_config import TestAppSettings

@pytest.fixture(scope="session", autouse=True)
def app_settings() -> TestAppSettings:
    """Override application settings for testing"""
    return TestAppSettings()

@pytest.fixture(scope="function")
async def http_client():
    """HTTP 클라이언트 픽스처"""
    async with httpx.AsyncClient(
        base_url="http://localhost:8000",
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
def mock_celery_app() -> Generator[MagicMock, None, None]:
    """Mock Celery application"""
    with pytest.MonkeyPatch.context() as mp:
        mock_app = MagicMock()
        mp.setattr("shared.celery_app.celery_app", mock_app)
        yield mock_app

@pytest.fixture
def existing_resume_keys():
    """기존에 생성된 이력서 키들"""
    return [
        "윤정은_1",
        "이민기_1", 
        "라이언_1"
    ]

@pytest.fixture
def test_user_data():
    """테스트용 사용자 데이터"""
    return {
        "current_skills": ["Python", "FastAPI"],
        "target_position": "Backend Developer"
    }

@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    with patch('redis.Redis') as mock:
        mock.return_value.get.return_value = b'{"status": "completed"}'
        mock.return_value.set = MagicMock()
        yield mock

@pytest.fixture
def mock_rabbitmq():
    """Mock RabbitMQ connection"""
    with patch('kombu.Connection') as mock:
        yield mock