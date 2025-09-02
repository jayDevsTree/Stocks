from database import base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from datetime import datetime
from Industry.industry_models import industry_table

class stock_table(base):
    __tablename__ = "Stock"
    
    stock_id = Column(Integer,primary_key=True,nullable=False)
    industry_id = Column(Integer,ForeignKey("Industry.industry_id"),nullable=False)
    stock_name = Column(String,nullable=False)
    stock_symbol = Column(String,nullable=True)
    stock_description = Column(String,nullable=True)
    current_price = Column(Integer,nullable=False)
    highest_price = Column(Integer,nullable=False)
    lowest_price = Column(Integer,nullable=False)
    stock_date = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text('now()'))
    
    