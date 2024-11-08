
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('str_engine')
def get_db_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind = engine) 
    return Session()

