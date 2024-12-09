
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import ORM_models
from ..database import get_db
from ..schemas import PostCreate, Post


router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(ORM_models.Post_ORM).all()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = ORM_models.Post_ORM(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=Post)
async def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    print(updated_post.model_dump())
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()