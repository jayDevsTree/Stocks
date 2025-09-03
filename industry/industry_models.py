from database import base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from datetime import datetime


class industry_table(base):
    __tablename__ = "industry"
    industry_id = Column(Integer,primary_key=True,nullable=False)
    industry_name = Column(String,nullable=False)
   