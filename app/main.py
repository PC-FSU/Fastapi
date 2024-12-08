import random
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Body,FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

from psycopg2 import sql



app = FastAPI()


# Connection parameters
DB_NAME = "social_media_database"
DB_USER = "pc19d"  # Replace with your PostgreSQL user
DB_PASSWORD = "password123"  # Replace with your PostgreSQL password
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    # Establish the connection
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Connected to the database!")
except Exception as e:
    print("Falied to connect to database!")
    print("Error:", e)
    


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}


@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM post """)
    posts = cursor.fetchall()
    return {'data' : posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}


@app.get('/posts/latest')
async def get_post():
    return {"post_details": my_posts[-1]}


@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    cursor.execute(
        """ SELECT * from post where id = %s""", (str(id))
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    return {"post_details": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(
        """ DELETE from post where id = %s returning * """, (str(id))
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE post SET title = %s, content = %s, published = %s where id = %s  RETURNING * """, (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    
    return {'data' : updated_post}