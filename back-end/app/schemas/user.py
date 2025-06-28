from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    MENTOR = "mentor"
    MENTEE = "mentee"

class MatchRequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

# 회원가입 요청
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRole

# 로그인 요청
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 로그인 응답
class LoginResponse(BaseModel):
    token: str

# 프로필 세부정보 - 멘토
class MentorProfileDetails(BaseModel):
    name: str
    bio: str
    imageUrl: str
    skills: List[str]

# 프로필 세부정보 - 멘티
class MenteeProfileDetails(BaseModel):
    name: str
    bio: str
    imageUrl: str

# 멘토 프로필
class MentorProfile(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    profile: MentorProfileDetails

# 멘티 프로필
class MenteeProfile(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    profile: MenteeProfileDetails

# 멘토 프로필 업데이트 요청
class UpdateMentorProfileRequest(BaseModel):
    id: int
    name: str
    role: UserRole
    bio: str
    image: str  # Base64 encoded image
    skills: List[str]

# 멘티 프로필 업데이트 요청
class UpdateMenteeProfileRequest(BaseModel):
    id: int
    name: str
    role: UserRole
    bio: str
    image: str  # Base64 encoded image

# 멘토 목록 아이템
class MentorListItem(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    profile: MentorProfileDetails

# 매칭 요청 생성
class MatchRequestCreate(BaseModel):
    mentorId: int
    menteeId: int
    message: str

# 매칭 요청
class MatchRequest(BaseModel):
    id: int
    mentorId: int
    menteeId: int
    message: str
    status: MatchRequestStatus

# 매칭 요청 (outgoing)
class MatchRequestOutgoing(BaseModel):
    id: int
    mentorId: int
    menteeId: int
    status: MatchRequestStatus

# 에러 응답
class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

class Config:
    from_attributes = True
