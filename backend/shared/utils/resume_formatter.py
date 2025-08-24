"""
이력서 데이터 포맷팅 공통 유틸리티
"""

from typing import Dict, Any


def format_resume_for_ai(
    resume_data: Dict[str, Any], 
    max_work_projects: int = 2,
    max_personal_projects: int = 1
) -> Dict[str, Any]:
    """
    이력서 데이터를 AI 프롬프트용으로 포맷팅
    
    Args:
        resume_data: 원본 이력서 데이터
        max_work_projects: 회사 프로젝트 최대 개수
        max_personal_projects: 개인 프로젝트 최대 개수
    
    Returns:
        AI 프롬프트용으로 포맷팅된 데이터
    """
    # 경력 정보
    total_months = resume_data.get("total_experience_months", 0)
    
    # 프로젝트 경험 추출 (핵심!)
    projects = []
    
    # 회사 프로젝트
    work_experiences = resume_data.get("work_experiences", [])
    for exp in work_experiences[:max_work_projects]:
        if exp.get("project_name"):
            project_info = _format_work_project(exp)
            if project_info:
                projects.append(project_info)
    
    # 개인 프로젝트  
    personal_projects = resume_data.get("personal_projects", [])
    for proj in personal_projects[:max_personal_projects]:
        project_info = _format_personal_project(proj)
        if project_info:
            projects.append(project_info)
    
    return {
        "name": resume_data.get("name", ""),
        "experience_months": total_months,
        "projects": "\n".join([f"- {project}" for project in projects])
    }


def _format_work_project(exp: Dict[str, Any]) -> str:
    """회사 프로젝트 포맷팅"""
    project_info = f"프로젝트: {exp['project_name']}"
    
    # 기술 스택 추가 (주요 4개만)
    if exp.get("tech_stack"):
        tech_list = exp["tech_stack"][:4]  # 주요 기술 4개만
        project_info += f" (기술: {', '.join(tech_list)})"
    
    # 주요 성과 추가 (첫 번째 성과만)
    if exp.get("achievements"):
        key_achievement = exp["achievements"][0] if exp["achievements"] else ""
        if key_achievement:
            # 너무 길면 축약
            if len(key_achievement) > 100:
                key_achievement = key_achievement[:100] + "..."
            project_info += f" - 주요 성과: {key_achievement}"
    
    return project_info


def _format_personal_project(proj: Dict[str, Any]) -> str:
    """개인 프로젝트 포맷팅"""
    project_info = f"개인 프로젝트: {proj.get('name', '')}"
    
    # 기술 스택 추가 (주요 4개만)
    if proj.get("tech_stack"):
        tech_list = proj["tech_stack"][:4]  # 주요 기술 4개만
        project_info += f" (기술: {', '.join(tech_list)})"
    
    # 주요 성과 추가 (첫 번째 성과만)
    if proj.get("key_achievements"):
        key_achievement = proj["key_achievements"][0] if proj["key_achievements"] else ""
        if key_achievement:
            # 너무 길면 축약
            if len(key_achievement) > 100:
                key_achievement = key_achievement[:100] + "..."
            project_info += f" - 주요 성과: {key_achievement}"
    
    return project_info


def format_resume_for_interview(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """면접 질문 생성용 이력서 포맷팅 (회사 2개 + 개인 1개)"""
    return format_resume_for_ai(
        resume_data, 
        max_work_projects=2, 
        max_personal_projects=1
    )


def format_resume_for_learning(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """학습 경로 생성용 이력서 포맷팅 (회사 2개 + 개인 2개)"""
    return format_resume_for_ai(
        resume_data, 
        max_work_projects=2, 
        max_personal_projects=2
    )
