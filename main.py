from fastapi import FastAPI, HTTPException, status, Depends
from users import users
from industry import industry
from stocks import stocks
from Transaction import tran

app = FastAPI()

app.include_router(users.router)
app.include_router(industry.router)
app.include_router(stocks.router)
app.include_router(tran.router)