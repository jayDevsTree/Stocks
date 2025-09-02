import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

load_dotenv(".env")

username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
hostname = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")


SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{db_password}@{hostname}/{db_name}"
while True:
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        with engine.connect() as conn:
            pass
        SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind = engine)
        base = declarative_base()
        print("Database Connection Sucessfull")
        break
    except Exception as e:
        print("Database Connection Failed")
        print("Error:", e)
        print("Retrying in 3 seconds...")
        time.sleep(3)
   
# this is define dependencies
def stock_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

