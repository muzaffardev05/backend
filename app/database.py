from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from app.config import *
from app.base import Base
import app.models
root_engine=create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}",echo=True)
with root_engine.begin() as c:
    c.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
engine=create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",echo=True)
SessionLocal=sessionmaker(bind=engine)

def init_db():
    
    Base.metadata.create_all(bind=engine)
