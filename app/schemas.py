from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional



# schema for auth routers 
class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None
    


# schema for user routers
class UserOut(BaseModel):
    email: EmailStr
    id: int
    class Config:
        orm_mode = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    

    
    

# schema for post routers
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
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True


# Schemas for voting functionality

class Vote(BaseModel):
    post_id: int
    direc: conint(le=1)