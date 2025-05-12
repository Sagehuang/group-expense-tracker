"""
定義 client.py 需用到的向 backend 溝通的 function

開發順序:
1. 確認需求: 從 Frontend 溝通文件得知 GUI 負責人開的需求 (在他們還沒寫需求時你也可以同步按照按鈕去想像他們會需要用到哪些 function 先寫好)
2. 實作 function: 一邊對照 API 溝通文件寫 (這樣你才知道要怎麼寫 route (/...), HTTP method 要用哪個 (GET, POST...), request 要傳什麼內容, 會收到什麼內容)
3. 測試: 暫時不管 GUI, 直接在 api_client.py 這個檔案的最後面寫測試 (你需要先 cd backend 然後 python app.py 啟動後端, 接著另外開一個 terminal cd frontend 然後 python api_client.py 執行這個檔案)
"""

import requests

BASE_URL = "http://localhost:5001/api"  # 設定 request 發到哪個位置 (這個 link 就是 Backend 運行的位置)


def sign_in(name):
    """
    傳送 name 給後端，若已有該 user 則登入，否則自動創建 user 後登入，回傳 user_info dict

    parameters:
    - name (str): user name

    return:
    - user_info (dict): 連線成功, 回傳使用者資訊包含 user id, name, groups
    - None: 連線失敗
    """
    # 寫 HTTP request 的 headers (我們的 case 應該統一都是寫這個可直接照抄)
    headers = {
        "Content-Type": "application/json"
    }
    # 寫要傳給 backend 的 request body (a dict)
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

        # print(f"Response content: {response.text}")  # debug 看從後端收到了什麼

        # 根據收到的 response 做處理
        if response.status_code == 200:  # 200 代表 OK 沒出問題
            return response.json()  # 回傳 user 資料, .json() 的用途是將 reponse 傳回來的 json 檔案轉成 dict
        else:
            print(f"Error! Server returned status code: {response.status_code}")  # 看出問題的 status code 是什麼, 可 google 看收到的數字對應的問題
            return None
    except requests.exceptions.RequestException as e:
        # 前面過程報錯的話就如何處理
        print("Request failed:", e)
        return None


# 測試範例
user_info = sign_in("Alice")
print(user_info)  # 期望要看到 Alice 的 id, name, group

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