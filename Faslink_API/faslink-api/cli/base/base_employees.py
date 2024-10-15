from fastapi import APIRouter , Depends, HTTPException , BackgroundTasks
import requests
from sqlalchemy.orm import Session
from ...dependencies import get_token_header
from ...database import SessionLocal, engine
from . import models, crud
from pydantic_core import from_json
import datetime
from datetime import datetime
from dateutil import parser

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/base",
    tags=["base"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/base-employees")
async def get_employees(db: Session = Depends(get_db)):
    url = 'https://hrm.base.vn/extapi/v1/employee/list'
    data_json = {'access_token':'3439-YKUA8Y8P58CNP5QGSD53DYADS24PHXCWXUYTB7LN4LX42PHJ8XH3N2GKZTW99YM2-QKGKDN6FBGNPHAUCQFD2SLBFLHAEYVS53TTLVTYV9NLDUXJ7PHDVKFH5MZY8S837' , 'charset':'unicode'}
    rs = requests.post(url, data= data_json)
    
    rs_dict = from_json(rs.text, allow_partial=True)

    rs_json = rs_dict.get('employees')
    
    for item in rs_json:       
        item['id'] = int(item['id'])
        item['first_name'] = item['first_name'].encode('utf-8').decode("utf-8", "ignore")
        item['last_name'] = item['last_name'].encode('utf-8').decode("utf-8", "ignore")
        item['title'] = item['title'].encode('utf-8').decode("utf-8", "ignore")
        item['name'] = item['name'].encode('utf-8').decode("utf-8", "ignore")
        item.pop('profile')
        item.pop('review')
        item.pop('bank')
        item.pop('basic_salary')
        item.pop('salary')
        item.pop('form')
        item['extracted_at'] = datetime.now()

    crud.create_BaseEmployee(rs_json,db)
    print(rs_json)   
    return rs_json