# shortener_app/crud.py

from sqlalchemy.orm import Session

from . import keygen, models, schemas


# function to interact with db, create read update delete (CRUD)
def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    # uses create_unique_random_key from keygen.py to get unique key not
    # already in use in db
    key = keygen.create_unique_random_key(db)
    # 
    #secret_key = keygen.create_random_key(length=8)
    # create random key and prefixes with unique random key, secret key will
    # always be unique but without econd query of db
    secret_key = f'{key}_{eygen.create_random_key(length=8)}'
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


# function to check if randomised key already exists in db or not
def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    # checks if models.URL.key == the queried URL key, checks if the entry is
    # active, returns the DB entry if both bool TRUE or returns NONE
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


# checks the db for an entry with the secret key, returns entry if found and
# returns NONE if not found
def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


# updates the number of clicks on a site, requires existing db as input to the
# function so won't work on non-existing dbs
def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    # increments clicks, commits changes, refreshes db, returns
    db_url.clicks += 1
    db.commit()
    db.refresh(deb_url)
    return db_url


# update db to remove url
def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    # sets db_url object from db using db and secret_key
    db_url = get_db_url_by_secret_key(db, secret_key)
    # if the object exists, sets is_active to false, commits changes, and
    # refreshes the db before returning the db object
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url