from database import engine,stock_db
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from . import tran_models,tran_schema

tran_models.base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

@app.get("/")
async def root():
    return {"Message": "This is a Transaction API"}

@router.post("/purchase", response_model=tran_schema.tran_show)
def buy_stock(from_stock_data: tran_schema.tran_create, db: Session = Depends(stock_db)):
    transaction = (
        db.query(tran_models.tran_table)
        .join(tran_models.tran_table.stock_all)
        .filter(tran_models.stock_table.stock_name == from_stock_data.stock_name)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with name {from_stock_data.stock_name} not found"
        )

    if from_stock_data.buy_volume > transaction.stock_remaining_volume:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock volume available"
        )

    total_price = from_stock_data.buy_volume * transaction.current_price

    # update stock volume
    transaction.stock_remaining_volume -= from_stock_data.buy_volume
    db.commit()
    db.refresh(transaction)

    return tran_schema.tran_show(
        stock_name=transaction.stock_name,
        buy_volume=from_stock_data.buy_volume,
        price_per_stock=transaction.current_price,
        total_price=total_price,
        remaining_volume=transaction.stock_remaining_volume
    )


# def tran_id_from_email(user_email_id : int, db: Session = Depends(stock_db)):
#     user_email = db.query(tran_models.tran_table).filter(tran_models.tran_table.users_all.email == user_email_id).first()
#     print(user_email)
#     return user_email

# def userID_from_email(user_email_id : int, db: Session = Depends(stock_db)):
#     user_email = db.query(tran_models.tran_table).filter(tran_models.tran_table.users_all.email).first()
#     print(user_email)
#     return user_email

# def fetch_stock_name(form_stock_data : tran_schema.tran_create,db : Session = Depends(stock_db)):
#     get_stockname = db.query(tran_models.tran_table).filter(tran_models.tran_table.stock_all.stock_name == form_stock_data.stock_name).first()
#     print(get_stockname)
#     return get_stockname
    

# @app.get("/transaction/{transaction_id}",response_model = tran_schema.tran_show)
# async def get_transaction(transaction_id : int , db : Session = Depends(stock_db)):
#     get_transaction = db.query(tran_models.tran_table).filter(tran_models.tran_table.transaction_id == transaction_id).first()
#     if get_transaction == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"Transaction with id {transaction_id} not found")
#     return get_transaction

# @app.get("/purchase")
# def get_stock(from_stock_data : tran_schema.tran_create, db : Session = Depends(stock_db)):
#     get_stock_name = db.query(tran_models.tran_table).filter(tran_models.tran_table.stock_all.stock_name == from_stock_data.stock_name).first()
#     if get_stock_name == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"Stock with name {from_stock_data.stock_name} not found")
#     form_stock_volume = from_stock_data.buy_volume
#     actual_volume = db.query(tran_models.tran_table).filter(tran_models.tran_table.stock_all.stock_volume).first()
    
