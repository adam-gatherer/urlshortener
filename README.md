# URL Shortener

## About

This is a project taken from [RealPython.com](https://www.realpython.com/). Uses [FastAPI](https://fastapi.tiangolo.com/), [Python](https://www.python.org/), and [Uvicorn](https://www.uvicorn.org/) to build a little URL shortener. I'll be modifying the project to add new features.

### To Do:

- ~~build project~~
- URL blacklist
- access keys
- custom URL redirects
- web interface
- come up with a cool name :^(

## Files

### config.py

Holds the configurations for the application. Base URL, environment name, database URL etc.

### crud.py

Handles all of the databse interactions. CRUD - create, read, update, delete.

### database.py

Creates the database, handles the session for working on it.

### __init__.py

Exists. Is empty. Tells Python shortener_app/ is a package.

### keygen.py

Creates unique keys for the redirect URL and admin access URL.

### main.py

Where the magic happens. Handles all API endpoints.

### models.py

Defines the databse tables and sets up their columns etc.

### schemas.py

Sets up the clases as children of the BaseModel class from Pydntic.