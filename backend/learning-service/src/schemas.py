"""
Learning Service 스키마 정의
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class LearningPathAnalysis(BaseModel):
    """이력서 분석 결과 스키마"""
    strengths: List[str] = Field(..., description="식별된 장점들")
    weaknesses: List[str] = Field(..., description="식별된 단점들")

class LearningPathItem(BaseModel):
    """학습 경로 아이템 스키마"""
    type: str = Field(..., description="학습 유형 (strength: 강점 심화, weakness: 약점 보완)")
    title: str = Field(..., description="학습 제목")
    description: str = Field(..., description="학습 설명 및 목표")
    reason: str = Field(..., description="왜 이 학습을 제시했는지 구체적 이유 (강점 심화 or 약점 보완)")
    resources: List[str] = Field(default=[], description="추천 학습 리소스/방법")
    link: str = Field(..., description="관련 학습 링크")

class LearningPathResponse(BaseModel):
    """학습 경로 추천 응답 스키마"""
    resume_id: str = Field(..., description="이력서 ID")
    learning_paths: List[LearningPathItem] = Field(..., min_items=3, max_items=8)
    generated_at: datetime = Field(..., description="생성 시간")
    summary: str = Field(..., description="학습 경로 전체 요약")

class LearningPathRequest(BaseModel):
    """학습 경로 생성 요청 스키마"""
    provider: str = Field(default="gemini", description="LLM 제공자 (gemini, openai, claude)")
    focus_areas: List[str] = Field(default=[], description="집중하고 싶은 영역 (선택사항)")
    target_role: str = Field(default="백엔드 개발자", description="목표 직무")
    time_commitment_hours_per_week: int = Field(default=10, description="주당 학습 가능 시간", ge=1, le=40)

class LearningPathCreateResponse(BaseModel):
    """학습 경로 생성 응답 스키마"""
    message: str = Field(..., description="응답 메시지")
    unique_key: str = Field(..., description="이력서 고유 키")
    provider: str = Field(..., description="사용된 LLM 제공자")
    model: str = Field(..., description="사용된 LLM 모델")
    analysis: LearningPathAnalysis = Field(..., description="이력서 장점/단점 분석 결과")
    summary: str = Field(..., description="학습 경로 전체 요약")
    learning_paths: List[LearningPathItem] = Field(..., description="생성된 학습 경로 목록")
    generated_at: datetime = Field(..., description="생성 시간")
