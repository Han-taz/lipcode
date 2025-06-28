from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import os
from decouple import config

# 환경변수 로딩 확인
print(f"🔧 [CONFIG] SECRET_KEY: {config('SECRET_KEY', default='default-secret')[:20]}...")
print(f"🔧 [CONFIG] ALGORITHM: {config('ALGORITHM', default='HS256')}")

from app.core.database import engine
from app.models import User, MatchRequest  # 모델 임포트
from app.core.database import Base
from app.routers import auth, users, mentors, match_requests

# 이미지 디렉토리 생성
os.makedirs("images", exist_ok=True)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mentor-Mentee Matching API",
    description="API for matching mentors and mentees in a mentoring platform",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/swagger-ui",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["User Profile"])
app.include_router(mentors.router, prefix="/api", tags=["Mentors"])
app.include_router(match_requests.router, prefix="/api", tags=["Match Requests"])

# Static files for images
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/")
async def root():
    """Redirect to Swagger UI"""
    print("🌐 [API] 루트 엔드포인트 접근됨")
    return RedirectResponse(url="/swagger-ui")

if __name__ == "__main__":
    print("🚀 [SERVER] 백엔드 서버 시작 중...")
    print("🔧 [SERVER] 포트: 8080")
    print("📡 [SERVER] CORS 허용 도메인: localhost:3000, 3001, 3002")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_level="info")
