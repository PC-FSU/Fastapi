
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import ORM_models, oauth2
from ..database import get_db
from ..utils import hash
from ..schemas import UserCreate, UserOut, Vote

router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: Vote, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    
    post = db.query(ORM_models.Post).filter(ORM_models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with id {vote.post_id} not found')
    
    vote_query = db.query(ORM_models.Vote).filter(ORM_models.Vote.post_id == vote.post_id, ORM_models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.direc == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'User {current_user.id} has already voted on post {vote.post_id}')
        new_vote = ORM_models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'User {current_user.id} has not liked the vote with {vote.post_id}')
        vote_query.delete(synchronize_session=False)
        db.commit()
    
        return {"message": "successfully deleted vote"} 