"""
Interview 마이크로서비스 메인 애플리케이션
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import os

from src.routes import router
from config import settings
from database import connect_to_mongo, close_mongo_connection
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
    title="Interview Service",
    description="AI-powered interview question generation service",
    version="1.0.0",
    docs_url="/api/v1/interview/docs",
    redoc_url="/api/v1/interview/redoc",
    openapi_url="/api/v1/interview/openapi.json",
    servers=[
        {"url": "http://api.localhost", "description": "API Gateway"},
        {"url": "http://localhost:8002", "description": "Direct Access (Development)"}
    ],
    lifespan=lifespan
)

# 에러 핸들러 등록
app.add_exception_handler(APIError, handle_api_error)
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, handle_validation_error)
app.add_exception_handler(Exception, handle_general_exception)

# 라우터 등록
app.include_router(router, prefix=settings.api_prefix, tags=["interview"])

# 테스트 페이지 라우트 추가
@app.get("/test")
async def get_test_page():
    """비동기 API 테스트 페이지"""
    # backend 디렉토리의 test_async_api.html 파일 반환  
    test_file_path = "/app/test_async_api.html"
    if os.path.exists(test_file_path):
        return FileResponse(test_file_path, media_type="text/html")
    else:
        return {"error": "Test page not found"}

@app.get("/")
async def root():
    """Interview 서비스 루트 엔드포인트"""
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
        port=8002,
        reload=True
    )
