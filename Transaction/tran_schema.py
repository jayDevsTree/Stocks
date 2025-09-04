from pydantic import BaseModel,EmailStr
from typing import Optional

class tran_create(BaseModel):
    # user_id:int
    # stock_id:int
    stock_name:str
    buy_volume:int
        
class tran_show(BaseModel):
    id:int
    email:EmailStr
    stock_name:str
    buy_volume:int
    current_value:float
    total_value:float
    buy_date:str
    
  
    
    

    

   