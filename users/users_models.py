from database import base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column,Integer,String,Boolean


class users_table(base):
    __tablename__ = 'users'
    
    user_id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable= False)
    email = Column(String,nullable=False,unique=True)
    password= Column(String)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text('now()'))
    
    
    
    
    
