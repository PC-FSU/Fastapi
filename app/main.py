import random
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Body,FastAPI, Response, status, HTTPException, Depends
from psycopg2 import sql
from sqlalchemy.orm import Session
from typing import List
from . import ORM_models
from .database import engine, get_db
from .utils import hash
from .schemas import PostCreate, Post, UserCreate, UserOut


# Create all tables in the database
ORM_models.Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}


@app.get('/posts', response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(ORM_models.Post_ORM).all()


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = ORM_models.Post_ORM(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{id}', response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', response_model=Post)
async def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    print(updated_post.model_dump())
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_users(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = ORM_models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.get('/users')
async def get_users(db: Session = Depends(get_db)):
    return db.query(ORM_models.User).all()


@app.get('/users/{id}', response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(ORM_models.User).filter(ORM_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    return user