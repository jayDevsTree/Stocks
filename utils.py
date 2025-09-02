from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt,JWTError
import os
from dotenv import load_dotenv

load_dotenv(".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

crypt_pass_make = CryptContext(schemes = ["bcrypt"], deprecated= "auto")

def hash(password:str):
    password_encrypt = crypt_pass_make.hash(password)
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
    encoded_jwt = jwt.encode(need_encode,SECRET_KEY,algorithm="HS256")
    return encoded_jwt
