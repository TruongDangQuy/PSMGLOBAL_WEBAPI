import http.client
import json
import logging
import http.server
import socketserver

# Cấu hình kết nối MSSQL (nếu bạn sử dụng pyodbc)
DATABASE_CONFIG = {
    'server': 'erp.thaiduongco.com,14330',
    'database': 'PMM_ERP_Dev',
    'username': 'PSMTrong',
    'password': 'PSMTrong@123',
    'driver': 'ODBC Driver 17 for SQL Server',
}

# Cấu hình API AiHR
API_URL = "hronline.thaiduongco.com/v4"
AUTH_URL = "/authorize"
REFRESH_URL = "/refresh"

APP_ID = "665eb95bda90441dc05b3063"
SECRET_KEY = "048e57abea7974886d82d8dd82063b92b7c1203e"


# Hàm lấy Access Token
def get_access_token():
    try:
        url = f"https://{API_URL}{AUTH_URL}"
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
                logging.error(f"Error in authorization (URL: {url}): {json_data.get('msg', 'Unknown error')}")
                return None
        else:
            logging.error(f"HTTP Error {response.status} at {url}: {data}")
            return None

    except Exception as e:
        logging.error(f"Error connecting to API at {url}: {e}")
        return None

# Hàm refresh token
def refresh_access_token(refresh_token):
    try:
        url = f"https://{API_URL}{REFRESH_URL}"
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
                logging.error(f"Error refreshing token (URL: {url}): {json_data.get('msg', 'Unknown error')}")
                return None
        else:
            logging.error(f"HTTP Error {response.status} at {url}: {data}")
            return None

    except Exception as e:
        logging.error(f"Error refreshing token at {url}: {e}")
        return None
	
# Hàm gọi API và chèn dữ liệu vào MSSQL
def fetch_data_from_db(controller, action, token, page=1, per_page=10):
    try:
        url = f"https://{API_URL}"
        conn = http.client.HTTPSConnection(API_URL)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "controller": controller,
            "action": action,
            "data": {},
            "page": page,
            "per_page": per_page
        })

        conn.request("POST", API_URL, body=payload, headers=headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        if response.status == 200:
            json_data = json.loads(data)
            if json_data.get('code') == 200:
                api_data = json_data['data']

                # Giả sử chèn vào MSSQL thành công
                logging.info(f"Data fetched from API at {url}.")
                return json_data['code'], json_data['data']
            else:
                logging.error(f"Error fetching data from API (URL: {url}): {json_data.get('msg', 'Unknown error')}")
                return None
        else:
            logging.error(f"HTTP Error {response.status} at {url}: {data}")
            return None

    except Exception as e:
        logging.error(f"Error fetching data from API at {url}: {e}")
        return None


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
            token_response = get_access_token()
            if token_response:
                access_token = token_response['access_token']
                refresh_token = token_response['refresh_token']
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
            token_response = get_access_token()
            if token_response and token_response['refresh_token']:
                new_token_response = refresh_access_token(token_response['refresh_token'])
                if new_token_response:
                    response = json.dumps({
                        "message": "Refresh token successful",
                        "new_access_token": new_token_response['access_token'],
                        "new_refresh_token": new_token_response['refresh_token']
                    })
                    self.send_response(200)
                else:
                    response = json.dumps({"error": "Failed to refresh token"})
                    self.send_response(500)
            else:
                response = json.dumps({"error": "No valid refresh token"})
                self.send_response(500)

            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

        elif self.path == '/call-api':
            token_response = get_access_token()
            if token_response:
                token = token_response['access_token']
                data = fetch_data_from_db('your_controller', 'your_action', token)
                response = json.dumps({
                    "message": "Data from API",
                    "data": data
                })
                self.send_response(200)
            else:
                response = json.dumps({"error": "Failed to call API"})
                self.send_response(500)

            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

# Tạo và chạy server
PORT = 5000
with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
