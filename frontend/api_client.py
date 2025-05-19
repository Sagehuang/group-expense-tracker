"""
定義 client.py 需用到的向 backend 溝通的 function

開發順序:
1. 確認需求: 從 Frontend 溝通文件得知 GUI 負責人開的需求 (在他們還沒寫需求時你也可以同步按照按鈕去想像他們會需要用到哪些 function 先寫好)
2. 實作 function: 一邊對照 API 溝通文件寫 (這樣你才知道要怎麼寫 route (/...), HTTP method 要用哪個 (GET, POST...), request 要傳什麼內容, 會收到什麼內容)
3. 測試: 暫時不管 GUI, 直接在 api_client.py 這個檔案的最後面寫測試 (你需要先 cd backend 然後 python app.py 啟動後端, 接著另外開一個 terminal cd frontend 然後 python api_client.py 執行這個檔案)
"""

import requests

BASE_URL = "http://localhost:5001/api"  # 設定後端主機與 API 前綴

#登入
def sign_in(name):
    """
    傳送 name 給後端，若已有該 user 則登入，否則自動創建 user 後登入，回傳 user_info dict

    parameters:
    - name (str): user name

    return:
    - user_info (dict): 連線成功, 回傳使用者資訊包含 user id, name, groups
    - None: 連線失敗
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": name
    }

    try:
        response = requests.post(
            f"{BASE_URL}/users/signin",
            headers=headers,
            json=payload
        )
    # 根據收到的 response 做處理
        if response.status_code == 200:
            return response.json()["id"]
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
# alice = sign_in("Alice")
# print(alice)

#新增花費
def add_expense(expense_data):
    """
    將新增的花費資訊傳入後端紀錄

    parameter:
    -expense_data (dictionary)：加入的一筆支出

    return:
    - x
    """
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "name": "Hotel",
        "amount": 200.0,
        "note": "2-night stay",
        "payer_id": 1,
        "participant_ids": [1, 2],
        "group_id": 1,
        "created_at": "2025-05-13T18:30:00",
        }
    
    try:
        response = requests.post(
            f"{BASE_URL}/expenses",
            headers=headers,
            json=payload
        )
    # 根據收到的 response 做處理
        if response.status_code == 201:
            print("支出新增成功")
        else:
            print(f"後端回傳錯誤狀態碼: {response.status_code}")
            print("回傳內容：", response.text)
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)
# ex = add_expense({
#         "name": "Hotel",
#         "amount": 300.0,
#         "note": "2-night stay",
#         "payer_id": 1,
#         "participant_ids": [1, 2],
#         "group_id": 1,
#         "created_at": "2025-05-13T18:30:00",
#         })
# print(ex)

#編輯花費
def edit_expense(expense_id,expense_data):
    """
    將修改的花費傳入後端

    parameter:
    -expense_data (dictionary)：修改的一筆支出

    return:
    - x
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
    "name": "Hotel (Updated)",
    "amount": 250.0,
    "note": "Updated note",
    "payer_id": 2,
    "participant_ids": [1, 2]
    }

    try:
        response = requests.put(
            f"{BASE_URL}/expenses/{expense_id}",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            print("支出編輯成功")
        else:
            print(f"後端回傳錯誤狀態碼: {response.status_code}")
            print("回傳內容：", response.text)
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)

# edit = edit_expense(4, 
#                     {
#   "name": "Hotel (Updated)",
#   "amount": 250.0,
#   "note": "Updated note",
#   "payer_id": 2,
#   "participant_ids": [1, 2]
# })
# print(edit)

# """2. 建立群組（同時將建立者加入群組）"""
# def add_group(group_name, creator_id):
#     try:
#         payload = {"name": group_name, "creator_id": creator_id}
#         response = requests.post(f"{BASE_URL}/groups", json=payload, headers={"Content-Type": "application/json"})
#         return response.status_code in [200, 201]
#     except Exception as e:
#         print("[add_group] failed:", e)
#         return False

# """ 3. 加入指定群組（需提供 group_id 與 user_id）"""
# def join_group(group_id, user_id):
#     try:
#         payload = {"user_id": user_id}
#         response = requests.post(f"{BASE_URL}/groups/{group_id}/join", json=payload, headers={"Content-Type": "application/json"})
#         return response.status_code == 200
#     except Exception as e:
#         print("[join_group] failed:", e)
#         return False


# """ 5. 查詢某個群組的所有支出"""
# def obtain_expense(group_id):
#     try:
#         response = requests.get(f"{BASE_URL}/groups/{group_id}/expenses")
#         if response.status_code == 200:
#             return response.json().get("all_expenses", [])
#         return []
#     except Exception as e:
#         print("[obtain_expense] failed:", e)
#         return []

'''
等到你徹底熟悉上面 function 的寫法就可以寫得更簡潔一點 以下是上面 function 的簡潔版:
def sign_in(name):
    """
    傳送 name 給後端，若已有該 user 則登入，否則自動創建 user 後登入，回傳 user_info dict

    parameters:
    - name (str): user name

    return:
    - user_info (dict): 連線成功, 回傳使用者資訊包含 user id, name, groups
    - None: 連線失敗
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": name
    }

    try:
        # 發送 HTTP request 並收到 response (HTTP method: POST, Route: /api/users/signin)
        response = requests.post(
            f"{BASE_URL}/users/signin",
            headers=headers,
            json=payload
        )

        # 根據收到的 response 做處理
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
'''

