"""
定義 client.py 需用到的向 backend 溝通的 function

開發順序:
1. 確認需求: 從 Frontend 溝通文件得知 GUI 負責人開的需求 (在他們還沒寫需求時你也可以同步按照按鈕去想像他們會需要用到哪些 function 先寫好)
2. 實作 function: 一邊對照 API 溝通文件寫 (這樣你才知道要怎麼寫 route (/...), HTTP method 要用哪個 (GET, POST...), request 要傳什麼內容, 會收到什麼內容)
3. 測試: 暫時不管 GUI, 直接在 api_client.py 這個檔案的最後面寫測試 (你需要先 cd backend 然後 python app.py 啟動後端, 接著另外開一個 terminal cd frontend 然後 python api_client.py 執行這個檔案)
"""

import requests
from datetime import datetime

BASE_URL = "http://localhost:5001/api"  # 後端 server 運行的位置


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


# 新增花費
def add_expense(created_at, name, amount, payer, participants, note, group_id):
    """
    新增一筆 expense

    parameters:
    - created_at (Datetime): 創建時間
    - name (str): expense 名稱
    - amount (int): 金額
    - payer (str): 付款人姓名
    - participants (list of str): 收款人姓名
    - note (str): 備註
    - group_id (int): 此 group 的 id

    return:
    - add_success (bool): 是否成功新增 expense
    """
    headers = {
        "Content-Type": "application/json"
    }
    # 這裡先暫時用 sign_in() 來跟後端拿 user id -> refactor: 請後端 API 再寫一個根據 user name 查詢 id 的 route
    payer_id = sign_in(payer)  # 把拿到的 user name 轉成 user id
    participant_ids = [sign_in(p) for p in participants]   # 把拿到的 user name 轉成 user id
    payload = {
        "name": name,
        "amount": float(amount),  # 把前端傳的 int 轉成 float 存給後端
        "note": note,
        "payer_id": payer_id,
        "participant_ids": participant_ids,
        "group_id": group_id,
        "created_at": created_at.isoformat()  # 將 datatime object 轉成 iso 時間格式的 str
    }

    try:
        response = requests.post(
            f"{BASE_URL}/expenses",
            headers=headers,
            json=payload
        )

        # 根據收到的 response 做處理
        if response.status_code == 201:
            return True
        else:
            print(f"後端回傳錯誤狀態碼: {response.status_code}")
            print("回傳內容：", response.text)
            return False
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)
        return False

# test
# add_success = add_expense(datetime(2025, 5, 22, 18, 30, 0), "Book", 300, "Alice", ["Alice", "Bob"], "note", 1)
# print("add_success:", add_success)  # True


# 編輯花費
def edit_expense(expense_id, name, amount, payer, participants, note):
    """
    編輯一筆既有 expense

    parameters:
    - expense_id (int): 此筆 expense 的 id
    - name (str): expense 名稱
    - amount (int): 金額
    - payer (str): 付款人姓名
    - participants (list of str): 收款人姓名
    - note (str): 備註
    - group_id (int): 此 group 的 id

    return:
    - edit_success (bool): 是否成功編輯 expense
    """
    headers = {
        "Content-Type": "application/json"
    }
    # 這裡先暫時用 sign_in() 來跟後端拿 user id -> refactor: 請後端 API 再寫一個根據 user name 查詢 id 的 route
    payer_id = sign_in(payer)  # 把拿到的 user name 轉成 user id
    participant_ids = [sign_in(p) for p in participants]   # 把拿到的 user name 轉成 user id
    payload = {
        "name": name,
        "amount": float(amount),  # 把前端傳的 int 轉成 float 存給後端
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
            return True
        else:
            print(f"後端回傳錯誤狀態碼: {response.status_code}")
            print("回傳內容：", response.text)
            return False
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)
        return False

# test
# edit_success = edit_expense(4, "2 Books", 600, "Bob", ["Alice, Bob"], "note")
# print("edit_success:", edit_success)  # True


# 新增群組
def add_group(group_name, user_id):
    """
    以 group name 創建一個新的 group，並新增 user 於該群組

    parameters:
    - group_name (str): 新增的群組名稱
    - user_id (int): 創建者 id

    return:
    - None
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": group_name,
        "creator_id": user_id
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
            return None
    except requests.exceptions.RequestException as e:
        print("發送失敗，錯誤為：", e)
        return None

# test
# new_group = add_group("Trip to Japan", 1)
# print("new_group:", new_group)  # None


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


# 取得 group 資訊
def get_groups_info(user_id):
    """
    根據 user id 查詢該 user 的所有 groups，回傳所有 groups 的 group id 和 group name

    parameter:
    - user_id (int)

    return:
    - current_groups (a list of dict): 使用者的所有 group, each dict looks like:
    {
        "group_id": 1 (str),
        "gorup_name": "Group A" (str)
    }
    """
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": user_id
    }

    try:
        response = requests.get(
            f"{BASE_URL}/users/{user_id}",
            headers=headers,
            json=payload
        )

        # 根據收到的 response 做處理
        if response.status_code == 200:
            data = response.json()
            current_groups = data["groups"]
            return current_groups
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# current_groups = get_groups_info(1)
# print("current_groups:", current_groups)


# 取得 group name
def obtain_group_name(group_id):
    """
    根據 group id 查詢該 group 的 name，回傳 group name

    parameter:
    - group_id (int)

    return:
    - group_name (str)
    """
    try:
        response = requests.get(f"{BASE_URL}/groups/{group_id}")
        if response.status_code == 200:
            data = response.json()
            group_name = data["name"]
            return group_name
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# group_name = obtain_group_name(3)
# print("group_name:", group_name)


# 取得 expense 的資訊
def get_expense_info(expense_id):
    """
    根據 expense id 查詢一筆 expense，回傳 expense 的資料

    parameter:
    - expense_id (int)

    return:
    - original_name (str)
    - original_amount (int)
    - orginial_note (str)
    - original_created_at (Datetime object)
    - original_payer (str)
    - original_participants (list of str)
    """
    try:
        response = requests.get(f"{BASE_URL}/expenses/{expense_id}")
        if response.status_code == 200:
            data = response.json()
            original_name = data["name"]
            original_amount = int(data["amount"])
            original_note = data["note"]
            original_created_at = datetime.fromisoformat(data["created_at"]).replace(microsecond=0)
            original_payer = data["payer"]["name"]
            original_participants = [user["name"] for user in data["participants"]]
            return original_name, original_amount, original_note, original_created_at, original_payer, original_participants
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# original_name, original_amount, original_note, original_created_at, original_payer, original_participants = get_expense_info(3)
# print("original_name:", original_name)
# print("original_amount:", original_amount)
# print("original_note:", original_note)
# print("original_created_at:", original_created_at)
# print("original_payer:", original_payer)
# print("original_participants:", original_participants)


# 顯示該群組的所有 expense
def obtain_expense(group_id):
    """
    根據 group id 查詢該 group 的所有 expenses，回傳所有 expenses

    parameter:
    - group_id(int)：欲顯示支出的目標群組 ID

    return:
    - group_expenses (a list of dict): 該 group 的所有 expenses, each dict looks like:
    {
        "name": "dinner" (str),
        "amount": 200 （int),
        "note": "sushi" (str),
        "created_at": 2025-05-13 18:30:00 (Datetime object),
        "payer": "Alice" (str),
        "expense_id": (int)
    }
    """
    group_expenses = []
    try:
        response = requests.get(f"{BASE_URL}/groups/{group_id}")
        if response.status_code == 200:
            data = response.json()

            expense_ids = [expense["id"] for expense in data["expenses"]]
            for expense_id in expense_ids:
                original_name, original_amount, original_note, original_created_at, original_payer, original_participants = get_expense_info(expense_id)
                expense_dict = {
                    "name": original_name,
                    "amount": original_amount,
                    "note": original_note,
                    "created_at": original_created_at,  # datetime object
                    "payer": original_payer,
                    "expense_id": expense_id
                }
                group_expenses.append(expense_dict)

            return group_expenses
        else:
            print(f"Error! Server returned status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# test
# group_expenses = obtain_expense(1)
# print("group_expenses:", group_expenses)


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
# group_name, members_list = get_members_info(1)
# print("group_name:", group_name)
# print("members_list:", members_list)


# 離開群組
def leave_group(user_id, group_id):
    """
    使用者離開 group，成功離開則回傳 True，查無 user 或 group 則回傳 False

    parameters:
    - user_id (int)
    - group_id (int)

    return:
    - leave_success (bool): 是否成功離開 group
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

# test
# leave_success = leave_group(3, 2)
# print("leave_success:", leave_success)  # True


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
