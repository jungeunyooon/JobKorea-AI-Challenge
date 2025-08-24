"""
Learning Service 메인 애플리케이션
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from config import settings
from database import connect_to_mongo, close_mongo_connection
from src.routes import router
from shared.utils.error_handler import (
    APIError,
    handle_api_error,
    handle_http_exception,
    handle_validation_error,
    handle_general_exception
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시
    await connect_to_mongo()
    yield
    # 종료 시
    await close_mongo_connection()

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Learning Service",
    description="AI-powered learning path recommendation service",
    version="1.0.0",
    docs_url="/api/v1/learning/docs",
    redoc_url="/api/v1/learning/redoc",
    openapi_url="/api/v1/learning/openapi.json",
    servers=[
        {"url": "http://api.localhost", "description": "API Gateway"},
        {"url": "http://localhost:8003", "description": "Direct Access (Development)"}
    ],
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 에러 핸들러 등록
app.add_exception_handler(APIError, handle_api_error)
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, handle_validation_error)
app.add_exception_handler(Exception, handle_general_exception)

# 라우터 등록
app.include_router(router, prefix=settings.api_prefix, tags=["learning"])

@app.get("/")
async def root():
    """Learning 서비스 루트 엔드포인트"""
    return {
        "service": settings.service_name,
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    """헬스 체크"""
    return {
        "service": settings.service_name,
        "status": "healthy"
    }

# 독립 실행 시
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )
