from typing import Annotated

from fastapi import Header, HTTPException, Depends
from .database import SessionLocal, engine
from .cli.auth import models, crud

from datetime import datetime

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# async def get_token_header(x_token: Annotated[str, Header()]):
#     if x_token != "Faslink-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def get_query_token(token: str):
#     if token != "Faslink-token":
#         raise HTTPException(status_code=400, detail="No faslink token provided")
    
#xtoken
async def get_token_header(x_token: Annotated[str, Header()]):
    db_xtoken = crud.valid_xtoken_in(xtoken=x_token, db = get_db())
    if db_xtoken is None:
        raise HTTPException(status_code=400, detail="X-Token is invalid")
    if db_xtoken.ExpiryDate < datetime.now():
        raise HTTPException(status_code=400, detail="X-Token is expired")

#token
async def get_query_token(token: str):
    db_token = crud.valid_token_in(token=token, db= get_db())
    if db_token is None:
        raise HTTPException(status_code=400, detail="Token is invalid")
    if db_token.ExpiryDate < datetime.now():
        raise HTTPException(status_code=400, detail="Token is expired")
    
