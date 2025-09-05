from database import engine,stock_db
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from . import tran_models,tran_schema
from users.users_models import users_table
from stocks.stock_models import stock_table
import helper
from datetime import datetime

tran_models.base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

@app.get("/")
async def root():
    return {"Message": "This is a Transaction API"}

@router.post("/purchase",status_code = status.HTTP_202_ACCEPTED,response_model=tran_schema.tran_show)
async def buy_stock(form_stock_data: tran_schema.tran_create,db: Session= Depends(stock_db),current_user = Depends(helper.get_current_user)):
    get_user = db.query(users_table).filter(users_table.user_id == current_user.user_id).first()
    get_stock = db.query(stock_table).filter(stock_table.stock_name == form_stock_data.stock_name).first()
    
    if get_user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"User with id {current_user.user_id} not found")
    if get_stock is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Stock with name {form_stock_data.stock_name} not found")
        
    if form_stock_data.buy_volume > get_stock.stock_remaining_volume:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = f"You can not buy more than {get_stock.stock_remaining_volume} stocks")
    if form_stock_data.buy_volume > get_stock.stock_total_volume:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = f"You can not buy more than {get_stock.stock_total_volume} stocks")
        
    get_stock.stock_remaining_volume = get_stock.stock_remaining_volume - form_stock_data.buy_volume
    # get_stock.stock_total_volume -= form_stock_data.buy_volume
    
    # stock_remaining_volume = tran_models.stock_table.stock_total_volume - form_stock_data.buy_volume
    # stock_table.stock_remaining_volume = stock_table.stock_total_volume - form_stock_data.buy_volume
    # purchase_price = get_stock.current_price * form_stock_data.buy_volume
    # purchase_price = tran_models.stock_table.current_price * form_stock_data.buy_volume
    # purchase_price = stock_table.current_price * form_stock_data.buy_volume
    
    purchse_price = get_stock.current_price * form_stock_data.buy_volume
    
    # db.commit()
    # db.refresh(stock_table)
    
    purchase_data = tran_models.tran_table(
        user_id = get_user.user_id,
        stock_id = get_stock.stock_id,
        buy_volume = form_stock_data.buy_volume,
        current_price = get_stock.current_price,
        total_price = purchse_price,
    )
    
    db.add(purchase_data)
    db.commit()
    db.refresh(purchase_data)
    # db.refrsh(stock_table)
    
    return tran_schema.tran_show(
        transaction_id=purchase_data.transaction_id,
        name=get_user.name,
        stock_name=get_stock.stock_name,
        buy_volume=purchase_data.buy_volume,
        current_price=purchase_data.current_price,
        total_price=purchase_data.total_price,
        stock_description=get_stock.stock_description, 
        transaction_date=purchase_data.transaction_date
    )
    