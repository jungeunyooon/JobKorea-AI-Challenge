"""
Interview 서비스 스키마
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class InterviewQuestion(BaseModel):
    """간소화된 면접 질문 스키마"""
    difficulty: str = Field(..., description="난이도 (easy|medium|hard)")
    topic: str = Field(..., description="주요 기술 키워드 (예: Kafka, Spring Boot, Redis)")
    question: str = Field(..., description="실제 질문 본문")
    what_good_answers_cover: List[str] = Field(..., description="좋은 답변이 포함해야 할 핵심 요소")

class InterviewQuestionsResponse(BaseModel):
    """면접 질문 생성 응답 스키마"""
    interview_id: str = Field(..., description="면접 질문 세션 ID")
    resume_id: str = Field(..., description="이력서 ID")
    unique_key: str = Field(..., description="이력서 고유 키")
    provider: str = Field(..., description="LLM 제공자")
    model: str = Field(..., description="사용된 LLM 모델")
    questions: List[InterviewQuestion] = Field(..., min_items=1, max_items=5)
    generated_at: datetime

class InterviewGenerateRequest(BaseModel):
    """면접 질문 생성 요청 (내부용)"""
    unique_key: str = Field(..., description="이력서 고유 키")

# Resume 관련 스키마 (외부 서비스에서 가져오는 데이터용)
class ResumeData(BaseModel):
    """이력서 데이터 (Resume 서비스에서 가져오는 형식)"""
    id: str
    name: str
    career_summary: str
    job_roles: List[str]
    tech_skills: List[str]
    years_experience: int
    unique_key: str
    created_at: datetime
    updated_at: datetime
