# shortener_app/main.py

import secrets

import validators
# imports FastAPI
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

# imports modules from this project
from . import crud, models, schemas
from .database import SessionLocal, engine
from .config import get_settings
#
from starlette.datastructures import URL

# instantiates FastAPI as app, used to interact with FastAPI
app = FastAPI()
# biinds database engine with models.Base.metadata.creatte_all(), if db
# doesn't yet exist then it will create it on first launch
models.Base.metadata.create_all(bind=engine)

# defines get_db(), creates  and yeilds new db session with each request,
# closes session once finished
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# function to return 404 if link not found
def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

# sets up bad request responses, takes in 'message'
def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


# makes FastAPI listen to the requests on the root path and returns message
@app.get("/")
def read_root():
    return "URL shortener API. No, I will not put a smiling emoticon here."


# makes FastAPI listen to requests for the shortened URL (url_key) 
@app.get("/{url_key}")
# function to return the redirect
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    # checks the db for active url, assigns result to db_url
    if db_url:= crud.get_db_url_by_key(db=db, url_key=url_key):
        # update the number of clicks
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_urL)
    else:
        raise_not_found(request)

# creates a response to URLs sent to the API via POST, runs create_url,
@app.post("/url", response_model=schemas.URLInfo)
# requires URLBase schema as argument, depends on database session, by passing
# get_db into Depends() a database session for the request is established and
# closed when the request is finished
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    # checks if target url is valid via validators  
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL.")
    ######## - NOT USED v
    # charset for key & secret_key, generates secret keys 
    #chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #key = "".join(secrets.choice(chars) for _ in range(5))
    #secret_key = "".join(secrets.choice(chars) for _ in range(8))
    # creates a database entry for the requested URL
    #db_url = models.URL(
    #    target_url=url.target_url, key=key, secret_key=secret_key
    #    )
    #db.add(db_url)
    #db.commit()
    #db.refresh(db_url)
    # adds key and secret_key to db_url match URLInfo
    ######## - NOT USED ^

    # usees create_db_url from crud.py to create the new db entry and uses the
    # fields key and secret_key to set the url and admin url
    db_url = crud.create_db_url(db=db, key=key)
    # returns the result of get_admin_info on db_url (a schema with the key
    # (url) and the secret key (admin url))
    return get_admin_info(db_url)


# function to get admin info, returns db_url with key and the admin endpoint
def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administratin info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

    

# defines a new API endpoint to get admin info
@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
    )
# takes in secret key, returns entry 
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)
    ):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        # as in create_url, runs db_url through get_admin_info and returns a
        # schema with key, secret key etc.
        return db_url
    else:
        raise_not_found(request)


# API endpoint to remove URL from db
@app.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f'Shortened URL deleted.\n({db_url.target_url})'
        return {"detail": message}
    else:
        raise_not_found(request)