from pydantic import BaseModel,EmailStr
from typing import Optional

class tran_create(BaseModel):
    id:int
    email:EmailStr
    volume:int
    current_value:float
    total_value:float
    buy_date:Optional[str] = None
    
class tran_show(tran_create):
    pass
    
    

    

   