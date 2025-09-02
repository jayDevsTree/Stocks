from database import base
from users.users_models import users_table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Integer,String,Boolean,Column,ForeignKey
from datetime import datetime
from stocks.stock_models import stock_table


class tran_table(base):
    __tablename__ = "Transaction"
    
    transaction_id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    stock_id = Column(Integer,ForeignKey("Stock.stock_id"),nullable=False)
    volume = Column(Integer,nullable=True)
    current_price = Column(Integer,nullable=False)
    total_price = Column(Integer,nullable=True)
    transaction_date = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text('now()'))
    
    
    
    