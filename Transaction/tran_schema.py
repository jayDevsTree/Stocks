from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class user_details(BaseModel):
    user_id:int
    name:str
    email:str
    
    class Config:
        orm_mode = True

class stock_details(BaseModel):
    stock_id:int
    stock_symbol:str
    stock_name:str
    stock_description:str
    
    class Config:
        orm_mode = True
    
class tran_create(BaseModel):
    stock_name:str
    buy_volume: int
    
class tran_update(tran_create):
    stock_name:Optional[str] = None
    buy_volume: Optional[int] = None 
    class Config:
        orm_mode = True
    
    
class tran_show(BaseModel):
    transaction_id: Optional[int]
    buy_volume:int
    current_price:int
    total_price:int
    transaction_date:Optional[datetime] 
    users: user_details
    stock: stock_details   
    
    class Config:
        orm_mode = True
    
    