from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Union
import json
import base64
import io
from PIL import Image

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.user import (
    MentorProfile, MenteeProfile, MentorProfileDetails, MenteeProfileDetails,
    UpdateMentorProfileRequest, UpdateMenteeProfileRequest, ErrorResponse
)

router = APIRouter()

@router.get("/me",
           response_model=Union[MentorProfile, MenteeProfile],
           responses={
               200: {"description": "User information retrieved successfully"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """현재 인증된 사용자 정보 조회"""
    image_url = f"/images/{current_user.role.value}/{current_user.id}"
    
    if current_user.role == UserRole.MENTOR:
        skills = json.loads(current_user.skills) if current_user.skills else []
        profile_details = MentorProfileDetails(
            name=current_user.name,
            bio=current_user.bio or "",
            imageUrl=image_url,
            skills=skills
        )
        return MentorProfile(
            id=current_user.id,
            email=current_user.email,
            role=current_user.role.value,
            profile=profile_details
        )
    else:
        profile_details = MenteeProfileDetails(
            name=current_user.name,
            bio=current_user.bio or "",
            imageUrl=image_url
        )
        return MenteeProfile(
            id=current_user.id,
            email=current_user.email,
            role=current_user.role.value,
            profile=profile_details
        )

@router.put("/profile",
           response_model=Union[MentorProfile, MenteeProfile],
           responses={
               200: {"description": "Profile updated successfully"},
               400: {"model": ErrorResponse, "description": "Bad request - invalid payload format"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def update_profile(
    profile_data: Union[UpdateMentorProfileRequest, UpdateMenteeProfileRequest],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 프로필 업데이트"""
    # 사용자 ID 확인
    if current_user.id != profile_data.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other user's profile"
        )
    
    # 프로필 정보 업데이트
    current_user.name = profile_data.name
    current_user.bio = profile_data.bio
    
    # 이미지 처리 (Base64 디코딩 및 저장)
    if profile_data.image:
        try:
            # Base64 이미지 디코딩
            image_data = base64.b64decode(profile_data.image)
            
            # 이미지 검증 및 리사이즈
            image = Image.open(io.BytesIO(image_data))
            if image.format not in ['JPEG', 'PNG']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only JPEG and PNG images are allowed"
                )
            
            # 이미지 크기 제한 확인 (500x500 ~ 1000x1000)
            width, height = image.size
            if width < 500 or height < 500 or width > 1000 or height > 1000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Image size must be between 500x500 and 1000x1000 pixels"
                )
            
            # 정사각형으로 크롭
            min_dimension = min(width, height)
            left = (width - min_dimension) / 2
            top = (height - min_dimension) / 2
            right = (width + min_dimension) / 2
            bottom = (height + min_dimension) / 2
            image = image.crop((left, top, right, bottom))
            
            # 이미지를 바이트로 변환
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format)
            img_byte_arr = img_byte_arr.getvalue()
            
            # 파일 크기 확인 (1MB 제한)
            if len(img_byte_arr) > 1024 * 1024:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Image size must be less than 1MB"
                )
            
            current_user.image_data = img_byte_arr
            current_user.image_filename = f"profile_{current_user.id}.{image.format.lower()}"
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid image data: {str(e)}"
            )
    
    # 멘토인 경우 스킬 업데이트
    if isinstance(profile_data, UpdateMentorProfileRequest):
        current_user.skills = json.dumps(profile_data.skills)
    
    db.commit()
    db.refresh(current_user)
    
    # 업데이트된 프로필 반환
    return get_current_user_info(current_user)

@router.get("/images/{role}/{user_id}",
           responses={
               200: {"description": "Profile image retrieved successfully"},
               401: {"model": ErrorResponse, "description": "Unauthorized - authentication failed"},
               500: {"model": ErrorResponse, "description": "Internal server error"}
           })
def get_profile_image(role: str, user_id: int, db: Session = Depends(get_db)):
    """프로필 이미지 조회"""
    user = db.query(User).filter(User.id == user_id, User.role == UserRole(role)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.image_data:
        # 데이터베이스에서 이미지 반환
        return Response(content=user.image_data, media_type="image/jpeg")
    else:
        # 기본 이미지 URL로 리다이렉트
        placeholder_url = f"https://placehold.co/500x500.jpg?text={role.upper()}"
        return Response(status_code=302, headers={"Location": placeholder_url})
