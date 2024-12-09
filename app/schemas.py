from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass



    

class UserCreate(BaseModel):
    email: EmailStr
    password: str


# These are response model output that will be sent out after api operation is done 
class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    email: EmailStr
    id: int
    class Config:
        orm_mode = True