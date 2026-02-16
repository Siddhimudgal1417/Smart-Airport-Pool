from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./ride_pool.db"

settings = Settings()
