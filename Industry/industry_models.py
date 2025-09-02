from database import base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Integer,String,Boolean,Column

class industry_table(base):
    __tablename__ = "Industry"
    
    industry_id = Column(Integer,primary_key=True,nullable=False)
    industry_name = Column(String,nullable=False)
    
