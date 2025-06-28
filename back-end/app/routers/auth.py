from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import SignupRequest, LoginRequest, LoginResponse, ErrorResponse
from app.models.user import User, UserRole
from app.utils.auth import get_password_hash, verify_password, create_access_token
import json
from datetime import timedelta

router = APIRouter()

@router.post("/signup", 
             status_code=status.HTTP_201_CREATED,
             responses={
                 201: {"description": "User successfully created"},
                 400: {"model": ErrorResponse, "description": "Bad request - invalid payload format"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    """사용자 회원가입"""
    print(f"DEBUG: Received signup data: {user_data}")
    print(f"DEBUG: Role type: {type(user_data.role)}, Role value: {user_data.role}")
    
    # 이메일 중복 확인
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 비밀번호 해싱
    hashed_password = get_password_hash(user_data.password)
    
    # 새 사용자 생성
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name,
        role=UserRole(user_data.role),
        bio="",  # 기본값
        skills="[]" if user_data.role == "mentor" else None  # 멘토인 경우 빈 배열
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}

@router.post("/login",
             response_model=LoginResponse,
             responses={
                 200: {"model": LoginResponse, "description": "Login successful"},
                 400: {"model": ErrorResponse, "description": "Bad request - invalid payload format"},
                 401: {"model": ErrorResponse, "description": "Unauthorized - login failed"},
                 500: {"model": ErrorResponse, "description": "Internal server error"}
             })
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """사용자 로그인"""
    # 사용자 조회
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=60)  # 1시간
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value
        },
        expires_delta=access_token_expires
    )
    
    return LoginResponse(token=access_token)
