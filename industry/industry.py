from database import engine,stock_db
from sqlalchemy.orm import Session
from . import industry_models,industry_schema
from fastapi import FastAPI,Response,status,HTTPException,Depends
import helper

industry_models.base.metadata.create_all(bind = engine)
# here need authentications means if a admin is logged and he make industires other like manager and employees have no access of this for that need authentications
app = FastAPI()

@app.get("/")
async def root():
    return {"Message":"This is a Industry Table Root Path"}

@app.post("/industry/create", status_code = status.HTTP_201_CREATED, response_model=industry_schema.industry_out)
async def create_industry(industry: industry_schema.industry_create, db: Session = Depends(stock_db),user_current: industry_models.industry_table = Depends(helper.get_current_user)):
    new_industry = industry_models.industry_table(**industry.dict())
    if db.query(industry_models.industry_table).filter(industry_models.industry_table.industry_name == industry.industry_name).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail= f"Industry with name {industry.industry_name} already exists")      
    db.add(new_industry)
    db.commit()
    db.refresh(new_industry)
    return new_industry

@app.delete("/industry/{industry_id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_industry(industry_id :int , db : Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
    get_industry = db.query(industry_models.industry_table).filter(industry_models.industry_table.industry_id == industry_id).first()
    if get_industry == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Industry with id {industry_id} not found")
    db.delete(get_industry)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.get("/industry", response_model = list[industry_schema.industry_out])
async def get_all_industries(db : Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
    industries = db.query(industry_models.industry_table).all()
    return industries

@app.get("/industry/{industry_id}",response_model = industry_schema.industry_out)
async def get_industry(industry_id : int , db : Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
    get_industry = db.query(industry_models.industry_table).filter(industry_models.industry_table.industry_id == industry_id).first()
    if get_industry == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Industry with id {industry_id} not found")
    return get_industry

@app.put("/industry/{industry_id}",response_model = industry_schema.industry_out)
async def update_industry(industry_id : int , form_industry: industry_schema.industry_create, db : Session = Depends(stock_db),current_user = Depends(helper.get_current_user)):
    db_get_industry = db.query(industry_models.industry_table).filter(industry_models.industry_table.industry_id == industry_id).first()
    if db_get_industry == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Industry with id {industry_id} not found")
    db_get_industry.industry_name = form_industry.industry_name
    db.commit()
    db.refresh(db_get_industry)
    return db_get_industry