from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.core.dependencies import get_current_mentee
from app.models.user import User, UserRole
from app.schemas.user import MentorListItem, MentorProfileDetails, ErrorResponse

router = APIRouter()

@router.get("/mentors",
           response_model=List[MentorListItem],
           responses={
               200: {"description": "Mentor list retrieved successfully"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def get_mentors(
    skill: Optional[str] = Query(None, description="Filter mentors by skill set"),
    orderBy: Optional[str] = Query(None, enum=["skill", "name"], description="Sort mentors by skill or name"),
    current_user: User = Depends(get_current_mentee),  # 멘티만 접근 가능
    db: Session = Depends(get_db)
):
    """멘토 목록 조회 (멘티 전용)"""
    # 기본 쿼리: 모든 멘토 조회
    query = db.query(User).filter(User.role == UserRole.MENTOR)
    
    # 스킬 필터링
    if skill:
        # JSON 배열에서 특정 스킬을 포함하는 멘토 찾기
        query = query.filter(User.skills.contains(f'"{skill}"'))
    
    # 정렬
    if orderBy == "name":
        query = query.order_by(User.name)
    elif orderBy == "skill":
        # 스킬 기준 정렬 (첫 번째 스킬 기준)
        query = query.order_by(User.skills)
    
    mentors = query.all()
    
    # 응답 형식으로 변환
    mentor_list = []
    for mentor in mentors:
        skills = json.loads(mentor.skills) if mentor.skills else []
        image_url = f"/images/mentor/{mentor.id}"
        
        profile_details = MentorProfileDetails(
            name=mentor.name,
            bio=mentor.bio or "",
            imageUrl=image_url,
            skills=skills
        )
        
        mentor_item = MentorListItem(
            id=mentor.id,
            email=mentor.email,
            role=mentor.role.value,
            profile=profile_details
        )
        mentor_list.append(mentor_item)
    
    return mentor_list
