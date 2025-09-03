from database import engine,stock_db
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from . import stock_models,stock_schema
import helper

stock_models.base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "This is a Root path of Stock Table"}


@router.post("/stocks/create", status_code = status.HTTP_201_CREATED, response_model = stock_schema.stock_out)
async def create_stock(stock: stock_schema.stock_create, db: Session = Depends(stock_db),user_current: stock_models.stock_table = Depends(helper.get_current_user)):
    new_stock = stock_models.stock_table(**stock.dict())
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock

@router.get("/stocks/all",response_model = list[stock_schema.stock_out])
async def get_all_stocks(db: Session = Depends(stock_db)):
    all_stocks = db.query(stock_models.stock_table).all()
    return all_stocks

@router.get("/stocks/{stock_id}",response_model = stock_schema.stock_out)
async def get_stock(stock_id : int , db : Session = Depends(stock_db),user_current: stock_models.stock_table = Depends(helper.get_current_user)):
    get_stock = db.query(stock_models.stock_table).filter(stock_models.stock_table.stock_id == stock_id).first()
    if get_stock == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"Stock with id {stock_id} not found")   
    return get_stock

@router.put("/stocks/{stock_id}",response_model = stock_schema.stock_out)
async def update_stock(stock_id : int, form_stock : stock_schema.stock_create, db : Session = Depends(stock_db),user_current: stock_models.stock_table = Depends(helper.get_current_user)):
    get_stock_from_db = db.query(stock_models.stock_table).filter(stock_models.stock_table.stock_id == stock_id).first()
    if get_stock_from_db == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            details= f"Stock with id {stock_id} not found")
        
    get_stock_from_db.stock_name = form_stock.stock_name
    get_stock_from_db.stock_symbol = form_stock.stock_symbol
    get_stock_from_db.stock_description = form_stock.stock_description
    get_stock_from_db.current_price= form_stock.current_price
    get_stock_from_db.highest_price= form_stock.highest_price
    get_stock_from_db.lowest_price = form_stock.lowest_price
    
    db.commit()
    db.refresh(get_stock_from_db)      
    return get_stock_from_db

@router.delete("/stocks/{stock_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(stock_id : int, db: Session = Depends(stock_db),user_current: stock_models.stock_table = Depends(helper.get_current_user)):
    get_stock = db.query(stock_models.stock_table).filter(stock_models.stock_table.stock_id == stock_id).first()
    if get_stock == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            details = f"Stock with id {stock_id} not found")
    db.delete(get_stock)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


