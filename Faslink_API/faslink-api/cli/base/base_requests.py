from fastapi import APIRouter , Depends, HTTPException

from ...dependencies import get_token_header

router = APIRouter(
    prefix="/base",
    tags=["base"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {
      "search": "",
      "email" : "thanhkieucong@gmail.com",
      "account_name": "TK",
      "job_title": "IT",
      "address": "Vuon Lai",
      "phone": {
              "phone": "0979419945",
              "call_code": "+84",
              "country_code": "VN",
              "country_name": "Vietnam"
          }
}

@router.post("/base-request")
async def get_requests():
    return fake_items_db