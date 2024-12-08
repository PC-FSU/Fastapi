import random
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Body,FastAPI, Response, status, HTTPException, Depends
from psycopg2 import sql
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .constant import Post
# Create all tables in the database
models.Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}


@app.get('/posts')
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post_ORM).all()
    return {'data' : posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post_ORM(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}


# @app.get('/posts/latest')
# async def get_post():
#     return {"post_details": my_posts[-1]}


# @app.get('/posts/{id}')
# async def get_post(id: int, response: Response):
#     cursor.execute(
#         """ SELECT * from post where id = %s""", (str(id))
#     )
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
#     return {"post_details": post}


# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int):
#     cursor.execute(
#         """ DELETE from post where id = %s returning * """, (str(id))
#     )
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put('/posts/{id}')
# async def update_post(id: int, post: Post):
#     cursor.execute(
#         """ UPDATE post SET title = %s, content = %s, published = %s where id = %s  RETURNING * """, (post.title, post.content, post.published, id)
#     )
#     updated_post = cursor.fetchone()
#     conn.commit()
    
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    
#     return {'data' : updated_post}