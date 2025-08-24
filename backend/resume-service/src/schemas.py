from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import re

class ContactInfo(BaseModel):
    """연락처 정보"""
    phone: Optional[str] = Field(None, description="전화번호")
    email: Optional[str] = Field(None, description="이메일")
    github: Optional[str] = Field(None, description="GitHub URL")
    linkedin: Optional[str] = Field(None, description="LinkedIn URL")
    portfolio: Optional[str] = Field(None, description="포트폴리오 URL")
    
    @validator('github', 'linkedin', 'portfolio')
    def validate_url(cls, v):
        if v and not re.match(r'^https?://', v):
            raise ValueError('URL must start with http:// or https://')
        return v

class WorkExperience(BaseModel):
    """경력 정보"""
    company: str = Field(..., description="회사명")
    position: str = Field(..., description="직책")
    duration: str = Field(..., description="근무 기간 (예: 2024.09 ~ 2024.12)")
    project_name: Optional[str] = Field(None, description="주요 프로젝트명")
    project_description: Optional[str] = Field(None, description="프로젝트 설명")
    tech_stack: List[str] = Field(default=[], description="사용한 기술 스택")
    achievements: List[str] = Field(default=[], description="주요 성과 및 기술적 업무")
    team_size: Optional[int] = Field(None, description="팀 규모", ge=1)

class PersonalProject(BaseModel):
    """개인 프로젝트"""
    name: str = Field(..., description="프로젝트명")
    duration: Optional[str] = Field(None, description="개발 기간")
    description: str = Field(..., description="프로젝트 설명")
    tech_stack: List[str] = Field(..., description="사용한 기술 스택")
    github_url: Optional[str] = Field(None, description="GitHub 저장소 URL")
    demo_url: Optional[str] = Field(None, description="데모/서비스 URL")
    key_achievements: List[str] = Field(default=[], description="주요 성과 및 기술적 도전")
    architecture_highlights: List[str] = Field(default=[], description="아키텍처 특이사항")
    
    @validator('github_url', 'demo_url')
    def validate_project_url(cls, v):
        if v and not re.match(r'^https?://', v):
            raise ValueError('URL must start with http:// or https://')
        return v

class Certification(BaseModel):
    """자격증 및 인증"""
    name: str = Field(..., description="자격증명")
    issuer: str = Field(..., description="발급기관")
    issue_date: str = Field(..., description="취득일 (YYYY.MM.DD)")
    expiry_date: Optional[str] = Field(None, description="만료일 (해당시)")
    credential_url: Optional[str] = Field(None, description="자격증 확인 URL")
    
    @validator('credential_url')
    def validate_credential_url(cls, v):
        if v and not re.match(r'^https?://', v):
            raise ValueError('URL must start with http:// or https://')
        return v

class TechnicalSkills(BaseModel):
    """기술 스킬 (세분화)"""
    programming_languages: List[str] = Field(default=[], description="프로그래밍 언어")
    frameworks: List[str] = Field(default=[], description="프레임워크")
    databases: List[str] = Field(default=[], description="데이터베이스")
    message_queue_caching: List[str] = Field(default=[], description="메시지 큐 및 캐싱")
    cloud_platforms: List[str] = Field(default=[], description="클라우드 플랫폼")
    devops_tools: List[str] = Field(default=[], description="DevOps 도구")
    monitoring_tools: List[str] = Field(default=[], description="모니터링 도구")
    others: List[str] = Field(default=[], description="기타 도구/기술")

class Activity(BaseModel):
    """관련 활동"""
    type: str = Field(..., description="활동 유형 (커뮤니티, 오픈소스, 스터디, 컨퍼런스 등)")
    name: str = Field(..., description="활동명/단체명")
    description: str = Field(..., description="활동 설명 및 역할")
    period: Optional[str] = Field(None, description="활동 기간")
    achievements: List[str] = Field(default=[], description="주요 성과 (수상, 발표 등)")
    url: Optional[str] = Field(None, description="관련 URL")
    
    @validator('url')
    def validate_activity_url(cls, v):
        if v and not re.match(r'^https?://', v):
            raise ValueError('URL must start with http:// or https://')
        return v

class Education(BaseModel):
    """교육 배경"""
    institution: str = Field(..., description="학교명")
    degree: str = Field(..., description="학위/과정명")
    major: str = Field(..., description="전공")
    period: str = Field(..., description="재학 기간")
    status: str = Field(..., description="상태 (졸업, 재학, 수료 등)")

class ResumeCreate(BaseModel):
    """풍부한 이력서 생성 스키마 (백엔드 개발자 전용)"""
    # 기본 정보
    name: str = Field(..., description="이름", min_length=1, max_length=50)
    contact: ContactInfo = Field(..., description="연락처 정보")
    summary: str = Field(..., description="한 줄 요약/소개", min_length=10, max_length=500)
    
    # 경력 정보
    work_experiences: List[WorkExperience] = Field(default=[], description="경력 사항")
    total_experience_months: int = Field(..., description="총 경력 (개월 단위)", ge=0)
    
    # 프로젝트
    personal_projects: List[PersonalProject] = Field(default=[], description="개인/팀 프로젝트")
    
    # 기술 스킬
    technical_skills: TechnicalSkills = Field(..., description="기술 스킬")
    
    # 자격증 및 활동
    certifications: List[Certification] = Field(default=[], description="자격증 및 인증")
    activities: List[Activity] = Field(default=[], description="관련 활동")
    education: List[Education] = Field(default=[], description="교육 배경")

class ResumeResponse(BaseModel):
    """풍부한 이력서 응답 스키마"""
    id: str = Field(..., description="이력서 ID")
    name: str
    contact: ContactInfo
    summary: str
    work_experiences: List[WorkExperience]
    total_experience_months: int
    personal_projects: List[PersonalProject]
    technical_skills: TechnicalSkills
    certifications: List[Certification]
    activities: List[Activity]
    education: List[Education]
    unique_key: str = Field(..., description="이름 기반 고유 키 (이름_1, 이름_2 등)")
    created_at: datetime
    updated_at: datetime
    
    # 편의성을 위한 계산 필드들
    @property
    def total_experience_years(self) -> float:
        """총 경력 연수 (소수점 포함)"""
        return round(self.total_experience_months / 12, 1)
    
    @property
    def all_tech_stack(self) -> List[str]:
        """모든 기술 스택 통합 리스트"""
        all_skills = []
        all_skills.extend(self.technical_skills.programming_languages)
        all_skills.extend(self.technical_skills.frameworks)
        all_skills.extend(self.technical_skills.databases)
        all_skills.extend(self.technical_skills.message_queue_caching)
        all_skills.extend(self.technical_skills.cloud_platforms)
        all_skills.extend(self.technical_skills.devops_tools)
        all_skills.extend(self.technical_skills.monitoring_tools)
        all_skills.extend(self.technical_skills.others)
        
        # 중복 제거 및 정렬
        return sorted(list(set(all_skills)))
    
    @property
    def project_count(self) -> int:
        """총 프로젝트 수 (경력 + 개인)"""
        work_projects = len([exp for exp in self.work_experiences if exp.project_name])
        return work_projects + len(self.personal_projects)


