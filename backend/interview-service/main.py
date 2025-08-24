"""
Interview 마이크로서비스 메인 애플리케이션
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.routes import router
from config import settings
from database import connect_to_mongo, close_mongo_connection

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

# 라우터 등록
app.include_router(router, prefix=settings.api_prefix, tags=["interview"])

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
