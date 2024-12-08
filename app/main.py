import random
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Body,FastAPI, Response, status, HTTPException, Depends
from psycopg2 import sql
from sqlalchemy.orm import Session
from . import ORM_models
from .database import engine, get_db
from .constant import Post
# Create all tables in the database
ORM_models.Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}


@app.get('/posts')
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(ORM_models.Post_ORM).all()
    return {'data' : posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = ORM_models.Post_ORM(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}


# @app.get('/posts/latest')
# async def get_post():
#     return {"post_details": my_posts[-1]}


@app.get('/posts/{id}')
async def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from post where id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    return {"post_details": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ DELETE from post where id = %s returning * """, (str(id))
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ UPDATE post SET title = %s, content = %s, published = %s where id = %s  RETURNING * """, (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    print(updated_post.model_dump())
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return {'data' : post_query.first()}