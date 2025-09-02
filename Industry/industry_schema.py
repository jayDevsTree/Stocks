from pydantic import BaseModel
from typing import Optional


class industry_create(BaseModel):
    id : int
    name: str
    
class industry_show(BaseModel):
    name :str