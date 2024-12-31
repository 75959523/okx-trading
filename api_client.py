import hmac
import base64
import json
import requests
from datetime import datetime, timezone

BASE_URL = "https://www.okx.com"
API_KEY = ''
SECRET_KEY = ''
PASSPHRASE = ''

def get_iso_timestamp():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def generate_signature(timestamp, method, request_path, body=''):
    message = f'{timestamp}{method}{request_path}{body}'
    mac = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), digestmod='sha256')
    return base64.b64encode(mac.digest()).decode('utf-8')

def send_request(method, request_path, body=None):
    timestamp = get_iso_timestamp()
    body_json = json.dumps(body) if body else ''
    signature = generate_signature(timestamp, method, request_path, body_json)
    headers = {
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}{request_path}"
    response = requests.request(method, url, headers=headers, json=body if body else None)
    return response.status_code, response.json()
