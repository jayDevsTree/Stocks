from pydantic import BaseModel
from typing import Optional


class stock_create(BaseModel):
    stock_id:Optional[int] = None
    industry_id:int
    stock_name:str
    stock_symbol:str
    stock_description:str
    current_price:int
    highest_price:int
    lowest_price:int
    
class stock_out(BaseModel):
    stock_name:str
    stock_symbol:str
    stock_description:str
    current_price:int
    highest_price:int
    lowest_price:int