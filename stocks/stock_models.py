from database import base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from datetime import datetime
from industry.industry_models import industry_table

class stock_table(base):
    
    __tablename__ = "stock"
    
    stock_id = Column(Integer,primary_key=True,nullable=False)
    industry_id = Column(Integer,ForeignKey("industry.industry_id"),nullable=False)
    stock_name = Column(String,nullable=False)
    stock_symbol = Column(String,nullable=True)
    stock_description = Column(String,nullable=True)
    current_price = Column(Integer,nullable=False)
    highest_price = Column(Integer,nullable=False)
    lowest_price = Column(Integer,nullable=False)
    stock_total_volume = Column(Integer,nullable=False)
    stock_remaining_volume = Column(Integer,nullable=False)
    is_deleted = Column(Boolean,nullable=False)
    deleted_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default = text('now()'))
    stock_date = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text('now()'))
    
    