
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import ORM_models
from ..database import get_db
from ..utils import hash
from ..schemas import UserCreate, UserOut

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_users(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = ORM_models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/')
async def get_users(db: Session = Depends(get_db)):
    return db.query(ORM_models.User).all()


@router.get('/{id}', response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(ORM_models.User).filter(ORM_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} not found.')
    return user
