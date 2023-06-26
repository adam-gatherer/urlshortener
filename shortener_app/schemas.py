# shortener_app/schemas.py

# imports BaseModel
from pydantic import BaseModel

# sets URLBase as a child of BaseModel, requires target_url as a string
class URLBase(BaseModel):
    target_url: str

# creates URL as a child of URLBase, sets is_active to be boolean and
# clicks to be int
class URL(URLBase):
    is_active: bool
    clicks: int

    # used to provide configurations to pydantic, orm is set to true to set
    # it to work with a database (object relational mapping)
    class Config:
        orm_mode = True

# defines URLInfo, requires two more strings; one for url and one for target
# url. By not using them in the URL class these values are not stored in the
# database 
class URLInfo(URL):
    url: str
    admin_url: str
