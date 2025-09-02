from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class users_create(BaseModel):
    name :str
    email:EmailStr
    password : Optional[str] = None
    
class user_out(BaseModel):
    user_id : int
    name:str
    email:str
    created_at:datetime
    
    class Config:
        orm_mode = True
        
class user_login(BaseModel):
    email:EmailStr
    password:str