from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Define the 'post' table
class Post_ORM(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False) # we are referencing to table, not class
    
    owner = relationship('User') # we are referencing to class, not the table
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    
# This is model that create composite key for vote-like system in our app. No user can like a post more than once, and multiple user can like a post.
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    
