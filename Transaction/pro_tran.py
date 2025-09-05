from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import tran_models, pro_tran_schema
from typing import List
from database import stock_db
import helper
from fastapi.responses import FileResponse
from . import invoice
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")
os.makedirs(INVOICE_DIR, exist_ok=True)

@router.post("/purchase", response_model=pro_tran_schema.tran_show)
async def buy_stock(form_data: pro_tran_schema.tran_create,db: Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
    # user_id comes from login user
    user_id = current_user.user_id  

    # stock we find using relationship query
    stock = db.query(tran_models.stock_table).filter(
        tran_models.stock_table.stock_name == form_data.stock_name
    ).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    if form_data.buy_volume > stock.stock_remaining_volume:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    stock.stock_remaining_volume -= form_data.buy_volume
    total_price = stock.current_price * form_data.buy_volume

    new_tran = tran_models.tran_table(
        user_id=user_id,
        stock_id=stock.stock_id,
        buy_volume=form_data.buy_volume,
        current_price=stock.current_price,
        total_price=total_price,
    )
    db.add(new_tran)
    db.commit()
    db.refresh(new_tran)
    # invoice.generate_invoice(new_tran)
    return new_tran


@router.get("/transactions/{tran_id}", response_model=pro_tran_schema.tran_show)
async def get_transaction(tran_id: int, db: Session = Depends(stock_db)):
    tran = db.query(tran_models.tran_table).filter(
        tran_models.tran_table.transaction_id == tran_id
    ).first()
    if not tran:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tran

@router.get("/transactions", response_model=list[pro_tran_schema.tran_show])
async def get_transactions(db: Session = Depends(stock_db)):
    return db.query(tran_models.tran_table).all()

@router.patch("/transactions/{tran_id}", response_model=pro_tran_schema.tran_show)
async def update_transaction(tran_id: int, form_data: pro_tran_schema.tran_update, db: Session = Depends(stock_db)):
    tran = db.query(tran_models.tran_table).filter(
        tran_models.tran_table.transaction_id == tran_id
    ).first()
    if not tran:
        raise HTTPException(status_code=404, detail="Transaction not found")

    stock = tran.stock  # via relationship

    if form_data.buy_volume:
        stock.stock_remaining_volume += tran.buy_volume  
        
        if form_data.buy_volume > stock.stock_remaining_volume:
            raise HTTPException(status_code=400, detail="Not enough stock available")
        
        stock.stock_remaining_volume -= form_data.buy_volume
        tran.buy_volume = form_data.buy_volume
        tran.total_price = tran.current_price * form_data.buy_volume

    db.commit()
    db.refresh(tran)
    return tran

@router.delete("/transactions/{tran_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_transaction(tran_id: int,db: Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
    tran = db.query(tran_models.tran_table).filter(
        tran_models.tran_table.transaction_id == tran_id,
        tran_models.tran_table.user_id == current_user.user_id,
        tran_models.tran_table.is_deleted == False
    ).first()
    if not tran:
        raise HTTPException(status_code=404, detail="Transaction not found or already deleted")
    
    
    tran.stock.stock_remaining_volume += tran.buy_volume

    tran.is_deleted = True

    db.commit()
    return

@router.delete("/transactions/{tran_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(tran_id: int, db: Session = Depends(stock_db)):
    tran = db.query(tran_models.tran_table).filter(
        tran_models.tran_table.transaction_id == tran_id
    ).first()
    if not tran:
        raise HTTPException(status_code=404, detail="Transaction not found")

    tran.stock.stock_remaining_volume += tran.buy_volume

    db.delete(tran)
    db.commit()
    return

@router.get("/transactions/recover/{tran_id}", response_model=pro_tran_schema.tran_show)
def recover_transaction(tran_id: int, db: Session = Depends(stock_db)):
    tran = db.query(tran_models.tran_table).filter(
        tran_models.tran_table.transaction_id == tran_id
    ).first()
    if not tran:
        raise HTTPException(status_code=404, detail="Transaction not found")

    tran.is_deleted = False

    db.commit()
    db.refresh(tran)
    return tran

@router.patch("/transactions/{tran_id}", response_model=pro_tran_schema.tran_show)
async def update_transaction(tran_id: int,form_data: pro_tran_schema.tran_update,db: Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
    tran = db.query(tran_models.tran_table).filter(
        tran_models.tran_table.transaction_id == tran_id,
        tran_models.tran_table.user_id == current_user.user_id  # only own transactions
    ).first()
    if not tran:
        raise HTTPException(status_code=404, detail="Transaction not found")

    stock = tran.stock  # relationship

    if form_data.buy_volume:
        
        stock.stock_remaining_volume += tran.buy_volume  

        if form_data.buy_volume > stock.stock_remaining_volume:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        stock.stock_remaining_volume -= form_data.buy_volume
        tran.buy_volume = form_data.buy_volume
        tran.total_price = tran.current_price * form_data.buy_volume

    db.commit()
    db.refresh(tran)
    return tran

@router.get("/invoice/{tran_id}")
def get_invoice(tran_id: int, db: Session = Depends(stock_db)):
    transaction = db.query(tran_models.tran_table).filter(tran_models.tran_table.transaction_id == tran_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {tran_id} not found")

   
    data = {
        "user": transaction.users.name,
        "email": transaction.users.email,
        "stock": transaction.stock.stock_name,
        "quantity": transaction.buy_volume,
        "price": transaction.current_price,
        "Date": transaction.transaction_date
    }
    

    # file path for saving
    file_path = os.path.join(INVOICE_DIR, f"invoice_{tran_id}.pdf")

    # generate PDF
    invoice.generate_invoice(data, file_path)

    return FileResponse(file_path, filename=f"invoice_{tran_id}.pdf", media_type="application/pdf")

