from sqlalchemy import Column, Integer, String, Text, LargeBinary, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(enum.Enum):
    MENTOR = "mentor"
    MENTEE = "mentee"

class MatchRequestStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    name = Column(String, nullable=False)
    bio = Column(Text)
    image_data = Column(LargeBinary)  # 프로필 이미지를 DB에 저장
    image_filename = Column(String)  # 이미지 파일명
    skills = Column(Text)  # JSON 형태로 저장 (멘토만 사용)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 멘토로서 받은 매칭 요청들
    received_requests = relationship("MatchRequest", foreign_keys="MatchRequest.mentor_id", back_populates="mentor")
    # 멘티로서 보낸 매칭 요청들  
    sent_requests = relationship("MatchRequest", foreign_keys="MatchRequest.mentee_id", back_populates="mentee")

class MatchRequest(Base):
    __tablename__ = "match_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mentee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(SQLEnum(MatchRequestStatus), default=MatchRequestStatus.PENDING)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 관계 설정
    mentor = relationship("User", foreign_keys=[mentor_id], back_populates="received_requests")
    mentee = relationship("User", foreign_keys=[mentee_id], back_populates="sent_requests")
