# shortener_app/database.py

# import sqlalchmey stuff to communicate with db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# create the db, set check_same_thread to false as SQLlite allows multiple
# requests at the same time
engine = create_engine(
        get_settings().db_url, connect_args={"check_same_thread": False}
        )
# creates the session for working on the db
SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
        )
Base = declarative_base()
