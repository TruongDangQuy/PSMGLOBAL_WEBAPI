from functools import lru_cache
from typing import Union
from fastapi import FastAPI,APIRouter,Depends
from .dependencies import get_query_token, get_token_header

from .cli.base import base_employees, base_requests , base_timeoffs, base_teams, base_areas, API_TD

#Add
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from typing_extensions import Annotated
from . import config
from fastapi.openapi.models import Server
@lru_cache
def get_settings():
    return config.Settings()

app = FastAPI(
    title="Your API Title",
    root_path="/v4",
    servers=[{
        "url": "https://hronline.thaiduongco.com/v4",
        "description": "Production server"
    }]
)



router = APIRouter(
    prefix="/v4",
    tags=["v4"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
        # "db_username": settings.db_username,
        # "db_password": settings.db_password,
        # "db_host": settings.db_host,
        # "db_database": settings.db_database,
    }

app.include_router(router)


app.include_router(base_requests.router)
app.include_router(base_employees.router)
app.include_router(base_timeoffs.router)
app.include_router(base_teams.router)
app.include_router(base_areas.router)
app.include_router(API_TD.router)


#models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

