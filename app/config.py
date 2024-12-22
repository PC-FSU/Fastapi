from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    # Configuration
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),  # Adjust path one directory up
        env_file_encoding="utf-8"
    )
    
settings = Settings()