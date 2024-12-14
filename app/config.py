from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Connection parameters
    DB_NAME: str
    DB_USER: str 
    DB_PASSWORD: str 
    DB_HOST: str
    DB_PORT: str

    # for jwt authentication
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Configuration
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),  # Adjust path one directory up
        env_file_encoding="utf-8"
    )

settings = Settings()
print(settings.model_dump())