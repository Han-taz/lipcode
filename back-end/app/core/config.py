from decouple import config

class Settings:
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./mentor_mentee.db")
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here-please-change-in-production")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60, cast=int)

settings = Settings()
