from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str = "sqlite:///./test.db"
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"

    class Config:
        env_file = ".env"

settings = Settings()
