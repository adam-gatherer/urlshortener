# shortener_app/keygen.py

# imports secrets module to 
import secrets
# imports string module to use in function
import string
from sqlalchemy.orm import Session
# imports crud.py for checking db for key
from . import crud

# creates a random key, what else is there to say
def create_random_key(length: int = 5) -> str:
    # creates list of all ascii uppercase characters and digits
    chars = string.ascii_uppercase + string.digits
    # returns a string of random characters "length" characters long
    return "".join(secrets.choice(chars) for _ in range (length))


# function to ensure key doesn't already exist, uses get_db_url_by_key from
# crud.py to query db with key
def create_unique_random_key(db: Session) -> str:
    # create the key
    key = create_random_key()
    # query the DB with random keys until get_db_url_by_key returns NONE
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    # return the unique key
    return key
