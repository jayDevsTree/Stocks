from database import engine,stock_db
from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import industry_models,industry_schema

industry_models.base.metadata.create_all(bind=engine)

app= FastAPI()

@app.get("/")
async def root():
    return {"Message":"This is a Root Path of Industry Table"}