from decouple import config

class Settings:
    DATABASE_URL: str = "sqlite:///./mentor_mentee.db"
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()

# 설정값 확인
print(f"🔧 [SETTINGS] SECRET_KEY: {settings.SECRET_KEY[:20]}...")
print(f"🔧 [SETTINGS] ALGORITHM: {settings.ALGORITHM}")
