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
            return response.json()
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
alice = sign_in("Alice")
print(alice)
# """ 1. 登入（若無則建立）"""
# def sign_in(name):
#     headers = {"Content-Type": "application/json"}
#     payload = {"name": name}
#     try:
#         response = requests.post(f"{BASE_URL}/users/signin", headers=headers, json=payload)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"[sign_in] failed: status code {response.status_code}")
#             return None
#     except Exception as e:
#         print("[sign_in] exception:", e)
#         return None

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

# """4. 新增支出（需提供 name, amount, payer_id, participant_ids, group_id）"""
# def add_expense(expense_data):
#     try:
#         url = f"{BASE_URL}/expenses"
#         print("📡 發送 POST 請求到：", url)
#         response = requests.post(url, json=expense_data, headers={"Content-Type": "application/json"})
        
#         if response.status_code in [200, 201]:
#             return True
#         else:
#             print("❌ [add_expense] response.status_code:", response.status_code)
#             print("❌ response.text:", response.text)
#             return False
#     except Exception as e:
#         print("🔥 [add_expense] exception:", e)
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

# """------------------ 🧪 測試區 ------------------"""
# if __name__ == "__main__":
#     print("🔹 登入 Alice")
#     alice = sign_in("Alice")
#     print(alice)

#     print("🔹 登入 Bob")
#     bob = sign_in("Bob")
#     print(bob)

#     alice_id = alice["id"]
#     bob_id = bob["id"]

#     print("🔹 建立群組：午餐小隊")
#     group_created = add_group("午餐小隊", creator_id=alice_id)
#     print("群組建立成功？", group_created)

#     print("🔹 Alice 加入群組")
#     joined_alice = join_group(group_id=1, user_id=alice_id)
#     print("加入成功？", joined_alice)

#     print("🔹 Bob 加入群組")
#     joined_bob = join_group(group_id=1, user_id=bob_id)
#     print("加入成功？", joined_bob)

#     print("🔹 新增支出（Alice 付款，Alice + Bob 均攤）")
#     test_expense = {
#         "name": "午餐",
#         "amount": 300.0,
#         "note": "義大利麵+飲料",
#         "payer_id": alice_id,
#         "participant_ids": [alice_id, bob_id],
#         "group_id": 1
#     }
#     added = add_expense(test_expense)
#     print("支出新增成功？", added)

#     print("🔹 查詢支出")
#     expenses = obtain_expense(1)
#     print(expenses)

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

