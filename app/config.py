from pydantic_settings import BaseSettings

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
    
    class Config:
        env_file = '.env'

settings = Settings()