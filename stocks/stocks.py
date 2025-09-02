from database import engine,stock_db
from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import stock_models,stock_schema

stock_models.base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is a Root path of Stock Table"}