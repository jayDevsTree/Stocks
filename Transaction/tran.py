from database import engine,stock_db
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session,joinedload
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

@router.get("/all/transactions",response_model=list[tran_schema.tran_show])
async def get_all_transactions(db:Session = Depends(stock_db)):
    return db.query(tran_models.tran_table).all()



@router.post("/purchase",status_code = status.HTTP_202_ACCEPTED,response_model=tran_schema.tran_show)
async def buy_stock(form_data: tran_schema.tran_create,db: Session= Depends(stock_db),current_user = Depends(helper.get_current_user)):
    # all_transactions = db.query(tran_models.tran_table).join(tran_models.tran_table.users).join(tran_models.tran_table.stock).all()
    user_id = current_user.user_id
    
    user = db.query(tran_models.users_table).filter(tran_models.users_table.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {user_id} not found")
    
    stock = db.query(tran_models.stock_table).filter(tran_models.stock_table.stock_name == form_data.stock_name).first()
    if stock is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Stock with name {form_data.stock_name} not found")
    
    # if user and stock:
    if form_data.buy_volume > stock.stock_total_volume:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"You can not buy more than {stock.stock_total_volume}")
    if form_data.buy_volume > stock.stock_remaining_volume:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"You can not buy more than {stock.stock_remaining_volume}")
    
    purchase = tran_models.tran_table(
        user_id = user_id,
        stock_id = stock.stock_id,
        buy_volume = form_data.buy_volume,
        current_price = stock.current_price,
        total_price = stock.current_price * form_data.buy_volume
    )
    stock.stock_remaining_volume -= form_data.buy_volume
    # print(all_transactions)
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase
    
    # tran.buy_volume = form_data.buy_volume
    # tran.current_price = stock.current_price
    # tran.total_price = stock.current_price * form_data.buy_volume
    # tran.user.user_id = user_id
    # tran.user.name = user.name
    # tran.user.email = user.email
    # tran.stock.stock_id = stock.stock_id
    # tran.stock.stock_name = stock.stock_name
    # tran.stock.stock_symbol = stock.stock_symbol
    # tran.stock.stock_description= stock.stock_description
    
    # return tran
    
@router.post("/trasaction/{transaction_id}", response_model = tran_schema.tran_show)
async def get_transaction(transaction_id: int,db: Session = Depends(stock_db)):
    get_tran = db.query(tran_models.tran_table).filter(tran_models.tran_table.transaction_id == transaction_id).first()
    if not get_tran:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Transaction with id {transaction_id} not found")
    return get_tran
   
# @router.patch("/trasaction/{transaction_id}", response_model = tran_schema.tran_show)
# async def update_transaction(transaction_id: int,form_data: tran_schema.tran_update,db: Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
#     update_tran = db.query(tran_models.tran_table).filter(tran_models.tran_table.transaction_id == transaction_id).first()
#     stock = db.query(tran_models.stock_table).filter(tran_models.stock_table.stock_name == update_tran.stock_name).first()
    
#     if update_tran is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Transaction with id {transaction_id} not found")
    
#     if stock is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Stock with name {update_tran.stock_name} not found")
    
#     if form_data.buy_volume > stock.stock_total_volume:
#         raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"You can not buy more than {stock.stock_total_volume}")
#     if form_data.buy_volume > stock.stock_remaining_volume:
#         raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"You can not buy more than {stock.stock_remaining_volume}")
    
#     updated = tran_models.tran_table(
#         user_id = current_user.user_id,
#         stock_id = stock.stock_id,
#         buy_volume = form_data.buy_volume,
#         current_price = stock.current_price,
#         total_price = stock.current_price * form_data.buy_volume
#     )
   
#     stock.stock_remaining_volume -= update_tran.buy_volume
    
#     db.commit()
#     db.refresh(update_tran)
#     return updated

@router.patch("/transaction/{transaction_id}", response_model=tran_schema.tran_show)
async def update_transaction(
    transaction_id: int,
    form_data: tran_schema.tran_update,
    db: Session = Depends(stock_db),
    current_user = Depends(helper.get_current_user)
):
    # Fetch transaction
    update_tran = db.query(tran_models.tran_table).filter(
        tran_models.tran_table.transaction_id == transaction_id
    ).first()

    if update_tran is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Transaction with id {transaction_id} not found")

    # Fetch stock
    stock = db.query(tran_models.stock_table).filter(
        tran_models.stock_table.stock_id == update_tran.stock_id
    ).first()

    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Stock with id {update_tran.stock_id} not found")

    # Check volume limits
    if form_data.buy_volume > stock.stock_total_volume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"You cannot buy more than {stock.stock_total_volume}")
    if form_data.buy_volume > stock.stock_remaining_volume + update_tran.buy_volume:
        # allow adjusting existing volume
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"You cannot buy more than {stock.stock_remaining_volume + update_tran.buy_volume}")

    
    new_total = stock.stock_remaining_volume + form_data.buy_volume
    prevoius_buy= new_total - stock.stock_total_volume
    real_total =  stock.stock_remaining_volume + prevoius_buy
    change_db_volume = real_total - form_data.buy_volume
    

    update_tran.user_id = current_user.user_id
    update_tran.buy_volume = form_data.buy_volume
    update_tran.current_price = stock.current_price
    update_tran.total_price = stock.current_price * form_data.buy_volume
    update_tran.transaction_date = datetime.utcnow()  

    stock.stock_remaining_volume = change_db_volume
    db.commit()
    db.refresh(update_tran)
    return update_tran

