from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
    
# Connection parameters
DB_NAME = "social_media_database"
DB_USER = "pc19d"  # Replace with your PostgreSQL user
DB_PASSWORD = "password123"  # Replace with your PostgreSQL password
DB_HOST = "localhost"
DB_PORT = "5432"