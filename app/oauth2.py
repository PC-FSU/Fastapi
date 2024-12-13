from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import datetime
from .schemas import TokenData
from .database import get_db
from . import ORM_models
from .config import settings


oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id_ = str(payload.get("user_id"))
        if id_ is None:
            raise credentials_exception
        token_data = TokenData(id=id_)
    except JWTError as e:
        raise credentials_exception from e
    return token_data

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not verify the credentials',
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = verify_access_token(token, credentials_exception)
    
    return db.query(ORM_models.User).filter(ORM_models.User.id == token.id).first()