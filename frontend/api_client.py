"""
定義 client.py 需用到的向 backend 溝通的 function

開發順序:
1. 確認需求: 從 Frontend 溝通文件得知 GUI 負責人開的需求 (在他們還沒寫需求時你也可以同步按照按鈕去想像他們會需要用到哪些 function 先寫好)
2. 實作 function: 一邊對照 API 溝通文件寫 (這樣你才知道要怎麼寫 route (/...), HTTP method 要用哪個 (GET, POST...), request 要傳什麼內容, 會收到什麼內容)
3. 測試: 暫時不管 GUI, 直接在 api_client.py 這個檔案的最後面寫測試 (你需要先 cd backend 然後 python app.py 啟動後端, 接著另外開一個 terminal cd frontend 然後 python api_client.py 執行這個檔案)
"""

import requests

BASE_URL = "http://localhost:5001/api"  # 設定後端主機與 API 前綴


# 登入
def sign_in(name):
    """
    傳送 name 給後端，若已有該 user 則登入，否則自動創建 user 後登入，回傳 user_info dict

    parameter:
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

# test
# user_id = sign_in("Alice")
# print("user_id:", user_id)
# user_id = sign_in("Jack")
# print("user_id:", user_id)
# a = sign_in("Alice")
# b = sign_in("Bob")
# c = sign_in("Chris")
# d = sign_in("Dog")
# print(a, b, c, d)

# 新增花費 # 已修改
def add_expense(created_at, name, amount, payer, participants, note, group_id):
    from datetime import datetime
    """
    將新增的花費資訊傳入後端紀錄

    parameter:
    -created_at (Datetime): 創建時間
    -name (str): expense 名稱
    -amount (int): 金額
    -payer (str): 付款人姓名
    -participants (list of str): 收款人姓名
    -note (str): 備註
    -group_id (int): 此 group 的 id

    return:
    - x
    """
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "amount": amount,
        "note": note,
        "payer_id": payer,
        "participant_ids": participants,
        "group_id": group_id, 
        "created_at": created_at,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/expenses",
            headers=headers,
            json=payload
        )
    # 根據收到的 response 做處理
        if response.status_code == 201:
            return response.json()["id"]
        else:
            print(f"後端回傳錯誤狀態碼: {response.status_code}")
            print("回傳內容：", response.text)
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)

# ex = add_expense(
#         "2025-05-22T18:30:00",
#         "Book",
#         300.0,
#         5,
#         [4, 5],
#         "",
#         8
#         )
# print(ex)


# 編輯花費 # 已修改
def edit_expense(expense_id, created_at, name, amount, payer, participant, note, group_id):
    """
    將修改的花費傳入後端

    parameter:
    -expense_id (int): 此筆 expense 的 id
    -created_at (Datetime): 創建時間
    -name (str): expense 名稱
    -amount (int): 金額
    -payer (str): 付款人姓名
    -participants (list of str): 收款人姓名
    -note (str): 備註
    -group_id (int): 此 group 的 id

    return:
    - x
    """
    payer_id = sign_in(payer)
    participant_ids = []
    for par in participant:
        id = sign_in(par)
        participant_ids.append(id)
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "amount": amount,
        "note": note,
        "payer_id": payer_id,
        "participant_ids": participant_ids
        }

    try:
        response = requests.put(
            f"{BASE_URL}/expenses/{expense_id}",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            return 
        else:
            print(f"後端回傳錯誤狀態碼: {response.status_code}")
            print("回傳內容：", response.text)
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)

# edit = edit_expense(17,
#   "2025-05-22T18:50:00",                  
#   "Book",
#    1250.0, 
#    "Dog",
#    ["Chris", "Dog"],
#    "",
#    8
# )
# print(edit)


# 新增群組 # 已修改
def add_group(group_name, user_id):
    """
    以 group name 創建一個新的 group，並新增 user 於該群組

    parameter:
    -group_name (str)：新增的群組名稱

    return:
    - x
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": group_name,
        "creator_id": user_id  # 使用者_ID
        }

    try:
        response = requests.post(
            f"{BASE_URL}/groups",
            headers=headers,
            json=payload
        )
        if response.status_code == 201:
            return None
        else:
            print(f"後端回傳錯誤狀態碼: {response.status_code}")
            print("回傳內容：", response.text)
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)
# new = add_group(
#   "Trip to Japan",
#   2   #使用者_ID
# )
# print(new)


# 加入群組
def join_group(group_id, user_id):
    """
    根據 group id 將當前 user 加入該 group，成功加入則回傳 True，查無 group 則回傳 False

    parameters:
    - group_id (int)：欲加入的群組 ID
    - user_id (int)：欲加入該 group_id 的 user (需不在該群組中)

    return:
    - join_success (bool): 是否成功加入 group
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "user_id": user_id
        }

    try:
        response = requests.post(
            f"{BASE_URL}/groups/{group_id}/join",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return True
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return False

# test
# join_success = join_group(1, 4)
# print("join_success:", join_success)


# 取得 expense 的資訊
def get_expense_info(expense_id):
    """
    根據 expense id 查詢一筆 expense，回傳 expense 的資料

    parameter:
    - expense_id (int)

    return:
    - original_item (str)
    - original_amount (int)
    - original_payer (str)
    - original_participants (list of str)
    - orginial_note (str)
    """
    try:
        response = requests.get(f"{BASE_URL}/expenses/{expense_id}")
        if response.status_code == 200:
            data = response.json()
            original_item = data["name"]
            original_amount = int(data["amount"])
            original_payer = data["payer"]["name"]
            original_participants = [user["name"] for user in data["participants"]]
            original_note = data["note"]
            original_time = data["created_at"]
            return original_item, original_amount, original_payer, original_participants, original_note, original_time
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# original_item, original_amount, original_payer, original_participants, original_note = get_expense_info(3)
# print("original_item:", original_item)
# print("original_amount:", original_amount)
# print("original_payer:", original_payer)
# print("original_participants:", original_participants)
# print("original_note:", original_note)


# 用來幫助 obtain_expense 回傳成 dict 的函數

    

# 顯示該群組的所有 expense
def obtain_expense(group_id):
    """
    根據 group id 查詢該 group 的所有 expenses，回傳所有 expenses

    利用後端的「查看群組詳情」

    parameter:
    -group_id(int)：欲顯示支出的目標群組 ID

    return:
    -{
        "name": "dinner" (str)
        "amount": 200 （int)
        "note": "sushi" (str)
        "created_at": 2025-05-13 18:30:00 (Datetime object)
        "payer": "Alice" (str)
        "expense_id": (int)
        }
    """
    # 無request body, 所以不用寫 headers, payload
    headers = {
        "Content-Type": "application/json"
    }
    expense_dict_list = []
    try:
        response = requests.get(f"{BASE_URL}/groups/{group_id}")
        if response.status_code == 200:
            data = response.json()
            expense_ids = [expense["id"] for expense in data["expenses"]]
            for exp_id in expense_ids:
                try:
                    original_item, original_amount, original_payer, original_participants, original_note, original_time = get_expense_info(exp_id)
                    expense_dict = {
                        "name": original_item,
                        "amount": original_amount,
                        "note": original_note,
                        "created_at": original_time,  # 這裡假設已經是 datetime 物件（不是就要轉）
                        "payer": original_payer,
                        "expense_id": exp_id
                    }
                    expense_dict_list.append(expense_dict)
                except Exception as e:
                    print(f"Error processing expense_id {exp_id}: {e}")
            return expense_dict_list
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# info = obtain_expense(8)
# print(info)


# 取得 member 資訊
def get_members_info(group_id):
    """
    根據 group id 查詢群組名稱和成員名稱

    parameter:
    - group_id (int)

    return:
    - group_name (str)
    - members_list (list of str)
    """
    try:
        response = requests.get(f"{BASE_URL}/groups/{group_id}")
        if response.status_code == 200:
            data = response.json()
            group_name = data["name"]
            members_list = [member["name"] for member in data["members"]]
            return group_name, members_list
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# group_name, members_list = get_members_info(8)
# print("group_name:", group_name)
# print("members_list:", members_list)


# 離開群組 
def leave_group(group_id, user_id):
    """
    使用者離開 group

    parameters:
    -user_id (int)
    -group_id (int)

    return:
    -x
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "user_id": user_id
        }

    try:
        response = requests.post(
            f"{BASE_URL}/groups/{group_id}/leave",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            return True
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return False
# leave = leave_group(8, 6)
# print(leave)


# 計算群組最終付款金額
def get_balance_info(group_id):
    """
    根據 group id 查詢 group 內所有 members 在結算後，應收應付的金額

    parameter:
    - group_id (int)

    return:
    - group_balance (list of dict): each dict looks like {"user_name": "Alice", "net_balance": -50}
    """
    try:
        response = requests.get(f"{BASE_URL}/groups/{group_id}/summary")
        if response.status_code == 200:
            data = response.json()
            group_balance = [
                {
                    "user_name": entry["user"]["name"],
                    "net_balance": int(entry["net_balance"])  # 將 float 轉成 int
                }
                for entry in data["summary"]
            ]
            return group_balance
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# group_balance = get_balance_info(2)
# print("group_balance:", group_balance)


# 找尋付款的最短路徑
def get_settle_info(group_id):
    """
    根據 group id 查詢欲結清群組所有款項的最短付款路徑

    parameters:
    - group_id (int)

    return:
    - group_settlement (list of dict): each dict looks like {"payer": "Alice", "receiver": "Bob", "amount": 50}
    """
    try:
        response = requests.get(f"{BASE_URL}/groups/{group_id}/settle")
        if response.status_code == 200:
            data = response.json()
            group_settlement = [
                {
                    "payer": s["payer"]["name"],
                    "receiver": s["receiver"]["name"],
                    "amount": int(s["amount"])  # 將 float 轉成 int
                }
                for s in data["settlements"]
            ]
            return group_settlement
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# group_settlement = get_settle_info(2)
# print("group_settlement:", group_settlement)


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
