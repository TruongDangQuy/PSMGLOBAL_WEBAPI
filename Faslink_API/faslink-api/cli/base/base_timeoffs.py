from fastapi import APIRouter , Depends, HTTPException , BackgroundTasks
import requests
from sqlalchemy.orm import Session
from ...dependencies import get_token_header
from ...database import SessionLocal, engine
from . import models, crud
from pydantic_core import from_json
import datetime, json
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

@router.post("/base-timeoffs")
async def get_timeoffs(start_date : str, end_date : str,  db: Session = Depends(get_db)):
    url = 'https://timeoff.base.vn/extapi/v1/timeoff/list'
    data_json = {'access_token':'3439-RZQFFKVTXZ9RQQGR77VHVS8M98YUJ2CR2FU33MGXTYX8PW7PVTHHYG3DUBYUK6R9-DFU3C9WKUNPH66LGU3AEBMUZJJK8M6WU39JKKFZSREYG8V2FVRYF92L9CJMYMJ6D' , 'charset':'unicode', 'start_date_from': start_date , 'end_date_to': end_date}
    rs = requests.post(url, data= data_json)
    rs_dict = from_json(rs.text, allow_partial=True)

    items_per_page = int(rs_dict.get('items_per_page'))
    total_items = int(rs_dict.get('total_items'))
    i = total_items//items_per_page
    remainder = total_items%items_per_page
    if remainder > 0: i = i + 1
    
    for x in range(i):
        rs_json = None
        rs_json = get_timeoff_loop(x , start_date, end_date)
        
        for item in rs_json:
            item['name'] = item['name'].encode('utf-8').decode("utf-8", "ignore")
            item['content'] = item['content'].encode('utf-8').decode("utf-8", "ignore")
            item['cut_off'] = item['cut_off'].encode('utf-8').decode("utf-8", "ignore")
            item['extracted_at'] = datetime.now()
        
        crud.create_BaseTimeoff(rs_json,db)
        x = x + 1

    return {"Response":"Successfully","Total Pages": i}

def get_timeoff_loop(i , start_date_from , end_date_to):
    url = 'https://timeoff.base.vn/extapi/v1/timeoff/list'
    data_json = {'access_token':'3439-RZQFFKVTXZ9RQQGR77VHVS8M98YUJ2CR2FU33MGXTYX8PW7PVTHHYG3DUBYUK6R9-DFU3C9WKUNPH66LGU3AEBMUZJJK8M6WU39JKKFZSREYG8V2FVRYF92L9CJMYMJ6D' , 'charset':'unicode', 'page':i, 'start_date_from': start_date_from , 'end_date_to': end_date_to}
    rs = requests.post(url, data =  data_json)

    rs_dict = from_json(rs.text, allow_partial=True)
    rs_json = rs_dict.get('timeoffs')
    
    return rs_json