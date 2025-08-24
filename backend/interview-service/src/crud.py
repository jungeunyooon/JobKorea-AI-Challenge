"""
Interview 서비스 CRUD 함수들
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import List, Optional, Dict, Any
from database import get_interview_collection, get_resumes_collection

async def get_resume_by_unique_key(unique_key: str) -> Optional[Dict[str, Any]]:
    """Resume 컬렉션에서 직접 이력서 조회"""
    resumes_collection = get_resumes_collection()
    resume = await resumes_collection.find_one({"unique_key": unique_key})
    if resume:
        resume["id"] = str(resume["_id"])
        del resume["_id"]
    return resume

async def get_interview_by_unique_key(unique_key: str) -> Optional[Dict[str, Any]]:
    """unique_key로 면접 질문 조회"""
    interview_collection = get_interview_collection()
    interview = await interview_collection.find_one({"unique_key": unique_key})
    if interview:
        interview["id"] = str(interview["_id"])
        del interview["_id"]
    return interview

async def create_interview_questions(interview_data: Dict[str, Any]) -> str:
    """면접 질문 저장"""
    interview_collection = get_interview_collection()
    result = await interview_collection.insert_one(interview_data)
    return str(result.inserted_id)

async def get_interview_questions_by_unique_key(unique_key: str) -> List[Dict[str, Any]]:
    """unique_key로 모든 면접 질문 조회"""
    interview_collection = get_interview_collection()
    cursor = interview_collection.find({"unique_key": unique_key}).sort("created_at", -1)
    interviews = await cursor.to_list(length=None)
    
    # ObjectId를 문자열로 변환
    for interview in interviews:
        interview["id"] = str(interview["_id"])
        del interview["_id"]
    
    return interviews