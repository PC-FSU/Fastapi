from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import datetime
from .schemas import TokenData
from .database import get_db
from . import ORM_models


oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # could be any long random text
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
    
    user = db.query(ORM_models.User).filter(ORM_models.User.id == token.id).first()
    
    return user