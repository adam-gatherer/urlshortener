# shortener_app/models.py
#
# describes the contents of the databse

# imports tools to build table
from sqlalchemy import Boolean, Column, Integer, String

# import Base to create URL class 
from .database import Base

# create URL class as a child of Base
class URL(Base):
    # set the table name
    __tablename__ = "urls"

    # sets the primary key for the table, the entry id
    id = Column(Integer, primary_key=True)
    # sets up the field for the key (eg, random string for url)
    key = Column(String, unique=True, index=True)
    # secret key is for users to manage their url redirects
    secret_key = Column(String, unique=True, index=True)
    # target url is not forced unique in case users request same target_URL
    target_url = Column(String, index=True)
    # boolean to determine if redirect active
    is_active = Column(Boolean, default=True)
    # counts how many times it's been clicked, starts at 0
    clicks = Column(Integer, default=0)
