# shortener_app/main.py

import secrets

import validators
# imports FastAPI
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# imports schemas from this project
from . import models, schemas
from .database import SessionLocal, engine

# instantiates FastAPI as app, used to interact with FastAPI
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# sets up bad request responses, takes in 'message'
def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

# makes FastAPI listen to the requests on the root path and returns message
@app.get("/")
def read_root():
    return "URL shortener API. No, I will not put a smiling emoticon here."

# creates a response to URLs sent to the API via POST, runs create_url
@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase):
    # checks if target url is valid via validators  
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL.")
    
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
        )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
        
    return f"TODO: Create database entry for: {url.target_url}"
