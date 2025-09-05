from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
    
class tran_create(BaseModel):
    stock_name:str
    buy_volume: int
    
class tran_show(BaseModel):
    transaction_id: Optional[int]
    name:str
    stock_name:str
    buy_volume:int
    current_price:int
    total_price:int
    stock_description:str
    transaction_date:Optional[datetime]
    
    class Config:
        orm_mode = True
    
    