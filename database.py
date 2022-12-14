import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL="sqlite:///./todos.db"
#SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres:admin@localhost/TodoApplicationDatabase"
SQLALCHEMY_DATABASE_URL=os.environ.get('DATABASE_URL')
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine= create_engine(
    #SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False}
    SQLALCHEMY_DATABASE_URL
)
#Instance of database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Database model
Base = declarative_base()
