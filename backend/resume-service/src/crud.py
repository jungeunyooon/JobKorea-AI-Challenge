"""
Resume Service CRUD 함수들
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from database import get_resumes_collection

async def create_resume(resume_data: Dict[str, Any]) -> str:
    """이력서 생성"""
    resumes_collection = get_resumes_collection()
    result = await resumes_collection.insert_one(resume_data)
    return str(result.inserted_id)

async def get_resume_by_unique_key(unique_key: str) -> Optional[Dict[str, Any]]:
    """unique_key로 이력서 조회"""
    resumes_collection = get_resumes_collection()
    resume = await resumes_collection.find_one({"unique_key": unique_key})
    if resume:
        resume["id"] = str(resume["_id"])
        del resume["_id"]
    return resume

async def get_resumes_by_name(name: str) -> List[Dict[str, Any]]:
    """사용자 이름으로 모든 이력서 조회"""
    resumes_collection = get_resumes_collection()
    cursor = resumes_collection.find({"name": name}).sort("created_at", -1)
    resumes = await cursor.to_list(length=None)
    
    # ObjectId를 문자열로 변환
    for resume in resumes:
        resume["id"] = str(resume["_id"])
        del resume["_id"]
    
    return resumes

async def update_resume(unique_key: str, update_data: Dict[str, Any]) -> bool:
    """이력서 업데이트"""
    resumes_collection = get_resumes_collection()
    update_data["updated_at"] = datetime.utcnow()
    result = await resumes_collection.update_one(
        {"unique_key": unique_key},
        {"$set": update_data}
    )
    return result.modified_count > 0

async def delete_resume(unique_key: str) -> bool:
    """이력서 삭제"""
    resumes_collection = get_resumes_collection()
    result = await resumes_collection.delete_one({"unique_key": unique_key})
    return result.deleted_count > 0