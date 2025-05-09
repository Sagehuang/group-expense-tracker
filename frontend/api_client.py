"""
定義 client.py 需用到之對 backend 溝通的 function
"""

import requests

BASE_URL = "http://localhost:5001/api"

def sign_in(name: str) -> dict | None:
    """傳送 name 給後端，如果已有該 name 則登入，否則自動創建後登入"""
    payload = {"name": name}
    headers = {
        "Content-Type": "application/json"
    }
    try:
        print(f"Sending request to {BASE_URL}/users/signin with payload: {payload}")  # debug
        response = requests.post(
            f"{BASE_URL}/users/signin",
            json=payload,
            headers=headers
        )
        print(f"Response status code: {response.status_code}")  # debug
        print(f"Response content: {response.text}")  # debug
        
        if response.status_code == 200:
            return response.json()  # 回傳 user 資料
        else:
            print(f"Server returned status code: {response.status_code}")  # debug
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None