from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
# from passlib.context import CryptContext
from app.core.config import settings
import uuid
import hashlib

# 비밀번호 해싱을 위한 컨텍스트 (임시로 bcrypt 대신 SHA256 사용)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증 (임시로 SHA256 사용)"""
    # return pwd_context.verify(plain_password, hashed_password)
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """비밀번호 해싱 (임시로 SHA256 사용)"""
    # return pwd_context.hash(password)
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 토큰 생성 (RFC 7519 준수)"""
    to_encode = data.copy()
    
    # 현재 시간
    now = datetime.utcnow()
    
    # 만료 시간 설정
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # RFC 7519 표준 클레임 추가
    to_encode.update({
        "iss": "mentor-mentee-app",  # issuer
        "sub": str(data.get("user_id")),  # subject (user ID)
        "aud": "mentor-mentee-frontend",  # audience
        "exp": expire,  # expiration time
        "nbf": now,  # not before
        "iat": now,  # issued at
        "jti": str(uuid.uuid4()),  # JWT ID
        # 커스텀 클레임
        "name": data.get("name"),
        "email": data.get("email"),
        "role": data.get("role")
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """JWT 토큰 검증"""
    try:
        print(f"🔍 [AUTH] 토큰 검증 시도: {token[:50]}...")
        print(f"🔧 [AUTH] SECRET_KEY: {settings.SECRET_KEY[:20]}...")
        print(f"🔧 [AUTH] ALGORITHM: {settings.ALGORITHM}")
        
        # audience 검증 옵션 추가
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}  # audience 검증 비활성화
        )
        print(f"✅ [AUTH] 토큰 검증 성공: {payload}")
        return payload
    except JWTError as e:
        print(f"❌ [AUTH] JWT 검증 에러: {e}")
        return None
