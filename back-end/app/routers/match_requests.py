from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_mentor, get_current_mentee
from app.models.user import User, UserRole, MatchRequest, MatchRequestStatus
from app.schemas.user import (
    MatchRequestCreate, MatchRequest as MatchRequestSchema, 
    MatchRequestOutgoing, ErrorResponse
)

router = APIRouter()

@router.post("/match-requests",
            response_model=MatchRequestSchema,
            responses={
                200: {"description": "Match request sent successfully"},
                400: {"model": ErrorResponse, "description": "Bad request - invalid payload or mentor not found"},
                401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
                500: {"model": ErrorResponse, "description": "Internal server error"}
            })
def create_match_request(
    request_data: MatchRequestCreate,
    current_user: User = Depends(get_current_mentee),  # 멘티만 접근 가능
    db: Session = Depends(get_db)
):
    """매칭 요청 생성 (멘티 전용)"""
    # 멘토 존재 확인
    mentor = db.query(User).filter(
        User.id == request_data.mentorId,
        User.role == UserRole.MENTOR
    ).first()
    
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mentor not found"
        )
    
    # 현재 사용자가 요청한 멘티 ID와 일치하는지 확인
    if current_user.id != request_data.menteeId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create request for other mentee"
        )
    
    # 이미 해당 멘토에게 요청을 보낸 적이 있는지 확인
    existing_request = db.query(MatchRequest).filter(
        MatchRequest.mentor_id == request_data.mentorId,
        MatchRequest.mentee_id == request_data.menteeId,
        MatchRequest.status.in_([MatchRequestStatus.PENDING, MatchRequestStatus.ACCEPTED])
    ).first()
    
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already have an active request to this mentor"
        )
    
    # 현재 다른 요청이 대기중인지 확인 (한 번에 하나의 요청만 가능)
    pending_request = db.query(MatchRequest).filter(
        MatchRequest.mentee_id == request_data.menteeId,
        MatchRequest.status == MatchRequestStatus.PENDING
    ).first()
    
    if pending_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send multiple requests simultaneously"
        )
    
    # 새 매칭 요청 생성
    new_request = MatchRequest(
        mentor_id=request_data.mentorId,
        mentee_id=request_data.menteeId,
        message=request_data.message,
        status=MatchRequestStatus.PENDING
    )
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return MatchRequestSchema(
        id=new_request.id,
        mentorId=new_request.mentor_id,
        menteeId=new_request.mentee_id,
        message=new_request.message,
        status=new_request.status.value
    )

@router.get("/match-requests/incoming",
           response_model=List[MatchRequestSchema],
           responses={
               200: {"description": "Incoming match requests retrieved successfully"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def get_incoming_match_requests(
    current_user: User = Depends(get_current_mentor),  # 멘토만 접근 가능
    db: Session = Depends(get_db)
):
    """받은 매칭 요청 목록 조회 (멘토 전용)"""
    requests = db.query(MatchRequest).filter(
        MatchRequest.mentor_id == current_user.id
    ).all()
    
    return [
        MatchRequestSchema(
            id=req.id,
            mentorId=req.mentor_id,
            menteeId=req.mentee_id,
            message=req.message,
            status=req.status.value
        )
        for req in requests
    ]

@router.get("/match-requests/outgoing",
           response_model=List[MatchRequestOutgoing],
           responses={
               200: {"description": "Outgoing match requests retrieved successfully"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def get_outgoing_match_requests(
    current_user: User = Depends(get_current_mentee),  # 멘티만 접근 가능
    db: Session = Depends(get_db)
):
    """보낸 매칭 요청 목록 조회 (멘티 전용)"""
    requests = db.query(MatchRequest).filter(
        MatchRequest.mentee_id == current_user.id
    ).all()
    
    return [
        MatchRequestOutgoing(
            id=req.id,
            mentorId=req.mentor_id,
            menteeId=req.mentee_id,
            status=req.status.value
        )
        for req in requests
    ]

@router.put("/match-requests/{request_id}/accept",
           response_model=MatchRequestSchema,
           responses={
               200: {"description": "Match request accepted successfully"},
               404: {"model": ErrorResponse, "description": "Match request not found"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def accept_match_request(
    request_id: int = Path(...),
    current_user: User = Depends(get_current_mentor),  # 멘토만 접근 가능
    db: Session = Depends(get_db)
):
    """매칭 요청 수락 (멘토 전용)"""
    # 요청 조회
    match_request = db.query(MatchRequest).filter(
        MatchRequest.id == request_id,
        MatchRequest.mentor_id == current_user.id
    ).first()
    
    if not match_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match request not found"
        )
    
    # 이미 수락된 요청이 있는지 확인 (한 명의 멘티만 수락 가능)
    existing_accepted = db.query(MatchRequest).filter(
        MatchRequest.mentor_id == current_user.id,
        MatchRequest.status == MatchRequestStatus.ACCEPTED
    ).first()
    
    if existing_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already have an accepted mentee"
        )
    
    # 요청 상태를 수락으로 변경
    match_request.status = MatchRequestStatus.ACCEPTED
    db.commit()
    db.refresh(match_request)
    
    return MatchRequestSchema(
        id=match_request.id,
        mentorId=match_request.mentor_id,
        menteeId=match_request.mentee_id,
        message=match_request.message,
        status=match_request.status.value
    )

@router.put("/match-requests/{request_id}/reject",
           response_model=MatchRequestSchema,
           responses={
               200: {"description": "Match request rejected successfully"},
               404: {"model": ErrorResponse, "description": "Match request not found"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def reject_match_request(
    request_id: int = Path(...),
    current_user: User = Depends(get_current_mentor),  # 멘토만 접근 가능
    db: Session = Depends(get_db)
):
    """매칭 요청 거절 (멘토 전용)"""
    # 요청 조회
    match_request = db.query(MatchRequest).filter(
        MatchRequest.id == request_id,
        MatchRequest.mentor_id == current_user.id
    ).first()
    
    if not match_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match request not found"
        )
    
    # 요청 상태를 거절로 변경
    match_request.status = MatchRequestStatus.REJECTED
    db.commit()
    db.refresh(match_request)
    
    return MatchRequestSchema(
        id=match_request.id,
        mentorId=match_request.mentor_id,
        menteeId=match_request.mentee_id,
        message=match_request.message,
        status=match_request.status.value
    )

@router.delete("/match-requests/{request_id}",
              response_model=MatchRequestSchema,
              responses={
                  200: {"description": "Match request cancelled successfully"},
                  404: {"model": ErrorResponse, "description": "Match request not found"},
                  401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
                  500: {"model": ErrorResponse, "description": "Internal server error"}
              })
def cancel_match_request(
    request_id: int = Path(...),
    current_user: User = Depends(get_current_mentee),  # 멘티만 접근 가능
    db: Session = Depends(get_db)
):
    """매칭 요청 취소 (멘티 전용)"""
    # 요청 조회
    match_request = db.query(MatchRequest).filter(
        MatchRequest.id == request_id,
        MatchRequest.mentee_id == current_user.id
    ).first()
    
    if not match_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match request not found"
        )
    
    # 요청 상태를 취소로 변경
    match_request.status = MatchRequestStatus.CANCELLED
    db.commit()
    db.refresh(match_request)
    
    return MatchRequestSchema(
        id=match_request.id,
        mentorId=match_request.mentor_id,
        menteeId=match_request.mentee_id,
        message=match_request.message,
        status=match_request.status.value
    )
