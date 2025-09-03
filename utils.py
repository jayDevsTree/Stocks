from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt,JWTError
import os
from dotenv import load_dotenv
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from users import users_schema,users_models
from database import stock_db
from sqlalchemy.orm import Session


oAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

load_dotenv(".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

crypt_pass_make = CryptContext(schemes = ["bcrypt"], deprecated= "auto") 

def hash(password:str):
    password_encrypt = crypt_pass_make.hash(password) # this encrypth password in database
    return password_encrypt

def verify(plain_password, hashed_password):
    return crypt_pass_make.verify(plain_password, hashed_password)


def create_access_token(data:dict,expires_delta : int| None = None):
    need_encode = data.copy()
    if expires_delta:
        expire =  datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    need_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(need_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        token_payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        # id : str = token_payload.get("user_id") # int
        id = token_payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = users_schema.token_data(id=id)
        
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oAuth2_scheme),db : Session = Depends(stock_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token,credentials_exception)
    user = db.query(users_models.users_table).filter(users_models.users_table.user_id == token_data.id).first()
    if user is None:
        raise credentials_exception
    return user
