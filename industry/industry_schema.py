from pydantic import BaseModel
from typing import Optional

class industry_create(BaseModel):
   
    industry_name: str
    
    class Config:
        # orm_mode = True
        from_attributes = True
        
        
class industry_out(BaseModel):
    industry_id: int
    industry_name: str