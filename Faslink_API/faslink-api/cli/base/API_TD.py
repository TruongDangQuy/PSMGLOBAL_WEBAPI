import http.client
import json
import logging
import http.server
import socketserver

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
from .models import API_TD


models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/hronline.thaiduongco.com",
    tags=["hronline.thaiduongco.com"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# Cấu hình API AiHR
API_URL = "hronline.thaiduongco.com"
AUTH_URL = "/v4/authorize"
REFRESH_URL = "/v4/refresh"

APP_ID = "665eb95bda90441dc05b3063"
SECRET_KEY = "048e57abea7974886d82d8dd82063b92b7c1203e"
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Hàm lấy Access Token
def get_access_token():
    try:
        conn = http.client.HTTPSConnection(API_URL)

        headers = {'Content-type': 'application/json'}

        payload = json.dumps({
            "application_id": APP_ID,
            "secret_key": SECRET_KEY
        })
        
        conn.request("POST", AUTH_URL, body=payload, headers=headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        if response.status == 200:
            json_data = json.loads(data)
            if json_data.get('code') == 200:
                access_token = json_data['data']['access_token']
                refresh_token = json_data['data']['refresh_token']
                token_type = json_data['data']['token_type']
                expires_in = json_data['data']['expires_in']

                logging.info(f"Authentication successful. Access Token: {access_token}")
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": token_type,
                    "expires_in": expires_in
                }
            else:
                logging.error(f"Error in authorization: {json_data.get('msg', 'Unknown error')}")
                return None
        else:
            logging.error(f"HTTP Error {response.status}: {data}")
            return None

    except Exception as e:
        logging.error(f"Error connecting to API: {e}")
        return None

# Hàm refresh token
def refresh_access_token(refresh_token):
    try:
        conn = http.client.HTTPSConnection(API_URL)
        headers = {
            "Authorization": f"Bearer {refresh_token}",
            "Content-Type": "application/json"
        }
        conn.request("POST", REFRESH_URL, headers=headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        if response.status == 200:
            json_data = json.loads(data)
            if json_data.get('code') == 200:
                access_token = json_data['data']['access_token']
                new_refresh_token = json_data['data']['refresh_token']
                token_type = json_data['data']['token_type']
                expires_in = json_data['data']['expires_in']

                logging.info(f"Token refreshed successfully. Access Token: {access_token}")
                return {
                    "access_token": access_token,
                    "refresh_token": new_refresh_token,
                    "token_type": token_type,
                    "expires_in": expires_in
                }
            else:
                logging.error(f"Error refreshing token: {json_data.get('msg', 'Unknown error')}")
                return None
        else:
            logging.error(f"HTTP Error {response.status}: {data}")
            return None

    except Exception as e:
        logging.error(f"Error refreshing token: {e}")
        return None

# Hàm gọi API và chèn dữ liệu vào MSSQL
@router.post("/v4")
def fetch_data_from_db(controller: str, action: str, token: str, db: Session = Depends(get_db), language: str = "vi", page: int = 1, per_page: int = 10):
    try:
        # Kết nối API
        conn = http.client.HTTPSConnection(API_URL)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Payload dựa theo Postman
        payload = json.dumps({
            "controller": controller,
            "action": action,
            "language": language,
            "data": {
                "selects": [
                    "staff_code",
                    "gender",
                    "email",
                    "phone"
                ],
                "where": [
                    {
                        "field": "gender",
                        "value": "male"
                    }
                ],
                "order": {
                    "key": "_id",
                    "value": "DESC"
                }
            },
            "page": page,
            "per_page": per_page
        })

        # Gửi request tới API
        conn.request("POST", "/v4", body=payload, headers=headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        if response.status == 200:
            json_data = json.loads(data)
            if json_data.get('code') == 0:
                api_data = json_data['data']['data']  # Dữ liệu bên trong `data` -> `data`

                # Xử lý dữ liệu từ API và thêm vào cơ sở dữ liệu MSSQL
                for item in api_data:
                    staff_code = item.get('staff_code', '')
                    gender = item.get('gender', '')
                    email = item.get('email', '')
                    phone = item.get('phone', '')
                    first_name = item['translate']['vi'].get('first_name', '')
                    last_name = item['translate']['vi'].get('last_name', '')
                    full_name = f"{first_name} {last_name}"

                    # Tạo một đối tượng mới tương ứng với bảng API_TD
                    new_record = API_TD(
                        staff_code=staff_code,
                        gender=gender,
                        email=email,
                        phone=phone,
                        first_name=first_name,
                        last_name=last_name,
                        full_name=full_name
                    )

                    # Thêm đối tượng mới vào session
                    db.add(new_record)

                # Commit session để lưu dữ liệu vào cơ sở dữ liệu
                db.commit()

                return json_data['code'], json_data['data']
            else:
                logging.error(f"Error fetching data from API: {json_data.get('msg', 'Unknown error')}")
                return {"error": json_data.get('msg', 'Unknown error')}
        else:
            logging.error(f"HTTP Error {response.status}: {data}")
            return {"error": f"HTTP Error {response.status}: {data}"}

    except Exception as e:
        logging.error(f"Error calling API or inserting data into MSSQL: {e}")
        db.rollback()  # Rollback nếu có lỗi xảy ra trong quá trình chèn dữ liệu
        return {"error": str(e)}


# Hàm trả về HTML cho menu chính
def get_menu_page():
    return """
<html>
    <head>
        <meta charset="utf-8">
        <title>PSM API Portal</title>
    </head>
    <body>
        <h1>PSM API Menu</h1>
        <ul>
            <button onclick="location.href='/authorize'">1. Authorize Token</button>
            <br><br>
            <button onclick="location.href='/refresh'">2. Refresh Token</button>
            <br><br>
            <button onclick="location.href='/call-api'">3. Call API</button>
        </ul>
    </body>
</html>
    """

# Hàm xử lý yêu cầu HTTP với http.server
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(get_menu_page().encode('utf-8'))

        elif self.path == '/authorize':
            access_token, refresh_token = get_access_token()
            if access_token:
                response = json.dumps({
                    "message": "Authorize successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
                self.send_response(200)
            else:
                response = json.dumps({"error": "Failed to authorize"})
                self.send_response(500)

            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/refresh':
            access_token, refresh_token = get_access_token()
            if refresh_token:
                new_access_token, new_refresh_token = refresh_access_token(refresh_token)
                response = json.dumps({
                    "message": "Refresh token successful",
                    "new_access_token": new_access_token,
                    "new_refresh_token": new_refresh_token
                })
                self.send_response(200)
            else:
                response = json.dumps({"error": "Failed to refresh token"})
                self.send_response(500)

            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/call-api':
            token = get_access_token()['access_token']  # Giả sử lấy token thành công
            data = fetch_data_from_db('your_controller', 'your_action', token)
            response = json.dumps({
                "message": "Data from API",
                "data": data
            })
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()


