from database import engine,stock_db
from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from . import tran_models,tran_schema

tran_models.base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"Message": "This is a Transaction API"}

