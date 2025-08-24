"""
Resume Service 메인 애플리케이션
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import connect_to_mongo, close_mongo_connection
from src.routes import router

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
    title="Resume Service",
    description="Resume management and validation service",
    version="1.0.0",
    docs_url="/api/v1/resumes/docs",
    redoc_url="/api/v1/resumes/redoc",
    openapi_url="/api/v1/resumes/openapi.json",
    servers=[
        {"url": "http://api.localhost", "description": "API Gateway"},
        {"url": "http://localhost:8001", "description": "Direct Access (Development)"}
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

# 라우터 등록
app.include_router(router, prefix=settings.api_prefix, tags=["resumes"])

@app.get("/")
async def root():
    """Resume 서비스 루트 엔드포인트"""
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
        port=8001,
        reload=True
    )
