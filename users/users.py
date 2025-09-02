from database import engine,stock_db
import utils
from fastapi import FastAPI,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from . import users_models,users_schema

users_models.base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/")
async def root():
    return{"Message":"This is a Users Table root Path"}

@app.get("/users")
async def get_all_users(db:Session = Depends(stock_db)):
    all_users = db.query(users_models.users_table).all()
    return all_users

@app.post("/createuser",status_code = status.HTTP_201_CREATED,response_model = users_schema.user_out)
async def create_user(user:users_schema.users_create,db: Session = Depends(stock_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = users_models.users_table(**user.dict())
    if db.query(users_models.users_table).filter(users_models.users_table.email == user.email).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"User with email {user.email} already exists")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}",response_model = users_schema.user_out)
async def get_user(user_id:int,db:Session = Depends(stock_db)):
    get_user = db.query(users_models.users_table).filter(users_models.users_table.user_id == user_id).first()
    if get_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {user_id} not found")
    return get_user

@app.put("/users/{user_id}",response_model = users_schema.user_out)
async def update_user(user_id:int,user:users_schema.users_create,db:Session = Depends(stock_db)):
    get_user = db.query(users_models.users_table).filter(users_models.users_table.user_id == user_id).first()
    if get_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {user_id} not found")
    get_user.name = user.name
    get_user.email = user.email
    get_user.password = user.password
    db.commit()
    db.refresh(get_user)
    return get_user

@app.delete("/users/{user_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int,db:Session = Depends(stock_db)):
    get_user = db.query(users_models.users_table).filter(users_models.users_table.user_id == user_id).first()
    if get_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {user_id} not found")
    db.delete(get_user)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.post("/users/login")
def login(user_credintial : users_schema.user_login,db : Session = Depends(stock_db)):
    fetchUser = db.query(users_models.users_table).filter(users_models.users_table.email==user_credintial.email).first()
   
    
    if not fetchUser:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = f"Invalid Credentials User Not Found")
    if not utils.verify(user_credintial.password,fetchUser.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = f"Invalid Credentials")
    return {"token":"create token"}




