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
    stock_total_volume:int
    is_deleted:Optional[bool] = False
    deleted_at:Optional[str] = None
    stock_remaining_volume:int
    
class stock_out(BaseModel):
    
    stock_name:str
    stock_symbol:str
    # stock_description:str
    current_price:int
    # highest_price:int
    # lowest_price:int
    stock_remaining_volume:int
    
class stock_out_only_for_patch(BaseModel):
    stock_id:Optional[int] = None
    industry_id:Optional[int] = None
    stock_name:Optional[str] = None
    stock_symbol:Optional[str] = None
    stock_description:Optional[str] = None
    current_price:Optional[int] = None
    highest_price:Optional[int] = None
    lowest_price:Optional[int] = None
    stock_total_volume:Optional[int] = None
    is_deleted:Optional[bool] = None
    deleted_at:Optional[str] = None
    stock_remaining_volume:Optional[int] = None
    