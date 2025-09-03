from database import engine,stock_db
import helper
from fastapi import FastAPI,Depends,HTTPException,status,Response,APIRouter
from sqlalchemy.orm import Session
from . import users_models,users_schema
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

users_models.base.metadata.create_all(bind = engine)
router = APIRouter()
app = FastAPI()

@router.get("/")
async def root():
    return{"Message":"This is a Users Table root Path"}


@router.get("/users",response_model = list[users_schema.user_out])
async def get_all_users(db:Session = Depends(stock_db)):
    all_users = db.query(users_models.users_table).all()
    return all_users


@router.post("/users/createuser",status_code = status.HTTP_201_CREATED,response_model = users_schema.user_out)
async def create_user(user:users_schema.users_create,db: Session = Depends(stock_db)):
   
    hashed_password = helper.hash(user.password)
    user.password = hashed_password
    new_user = users_models.users_table(**user.dict())
    if db.query(users_models.users_table).filter(users_models.users_table.email == user.email).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"User with email {user.email} already exists")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}",response_model = users_schema.user_out)
async def get_user(user_id:int,db:Session = Depends(stock_db),user_current: users_models.users_table = Depends(helper.get_current_user)):
    get_user = db.query(users_models.users_table).filter(users_models.users_table.user_id == user_id).first()
    if get_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {user_id} not found")
    return get_user


@router.put("/users/{user_id}",response_model = users_schema.user_out)
async def update_user(user_id:int,user:users_schema.users_create,db:Session = Depends(stock_db),user_current: users_models.users_table = Depends(helper.get_current_user)):
    get_user = db.query(users_models.users_table).filter(users_models.users_table.user_id == user_id).first()
    if get_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {user_id} not found")
    get_user.name = user.name
    get_user.email = user.email
    get_user.password = user.password
    db.commit()
    db.refresh(get_user)
    return get_user


@router.delete("/users/{user_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int,db:Session = Depends(stock_db),user_current: users_models.users_table = Depends(helper.get_current_user)):
    get_user = db.query(users_models.users_table).filter(users_models.users_table.user_id == user_id).first()
    if get_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User with id {user_id} not found")
    db.delete(get_user)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
 
 
@router.post("/users/login",response_model = users_schema.token)
def login_form(user_form_info : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(stock_db)): 
    # in OAuth2PasswordRequestForm two fields username and password so here username is email  
    in_db_user = db.query(users_models.users_table).filter(users_models.users_table.email == user_form_info.username).first()
     # the use-info password need to encrypyt
    
    if not in_db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid Credentials User Not Found")
        
    if not helper.verify(user_form_info.password,in_db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid Password")  
            
    access_token = helper.create_access_token(data={"user_id":in_db_user.user_id},expires_delta = timedelta(minutes=5))
    
    return {"access_token":access_token,
            "token_type":"bearer",
            "name": in_db_user.name}# this last ignore cause response model
    
app.include_router(router)
# @app.post("/users/login")
# def login(user_credintial : users_schema.user_login,db : Session = Depends(stock_db)):
#     fetchUser = db.query(users_models.users_table).filter(users_models.users_table.email==user_credintial.email).first()
     
#     if not fetchUser:
#         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
#                             detail = f"Invalid Credentials User Not Found")
#     if not utils.verify(user_credintial.password,fetchUser.password):
#         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
#                             detail = f"Invalid Credentials")
#     access_token = utils.create_access_token(data={"user_id":fetchUser.user_id},expires_delta = timedelta(minutes=30))
    
#     return {"token":access_token,
#             "token_type":"bearer"}