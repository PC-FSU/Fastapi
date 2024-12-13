
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import ORM_models, oauth2
from ..database import get_db
from ..schemas import PostCreate, Post


router = APIRouter(prefix='/posts', tags=['Posts'])



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    new_post = ORM_models.Post_ORM(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db),  current_user: int =  Depends(oauth2.get_current_user)):
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')
    return post

@router.get('/', response_model=List[Post])
async def get_posts(db: Session = Depends(get_db),  current_user: int =  Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= ''):
    return db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.title.contains(search)).offset(skip).limit(limit).all()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    post = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')

    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action',
        )

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=Post)
async def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    post_query = db.query(ORM_models.Post_ORM).filter(ORM_models.Post_ORM.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found.')

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action',
        )
    
    print(updated_post.model_dump())
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()