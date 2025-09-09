from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class user_show(BaseModel):
    user_id: int
    name: str
    email: str
    class Config:
        orm_mode = True

class stock_show(BaseModel):
    stock_id: int
    stock_symbol: str
    stock_name: str
    stock_description: str
    class Config:
        orm_mode = True



class tran_create(BaseModel):
    stock_name: str
    buy_volume: int

class tran_update(BaseModel):   
    buy_volume: Optional[int] = None

class tran_show(BaseModel):
    transaction_id: int
    buy_volume: int
    current_price: int
    total_price: int
    transaction_date: datetime
    users: user_show
    stock: stock_show
    class Config:
        orm_mode = True
