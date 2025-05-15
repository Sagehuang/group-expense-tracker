#這個code沒有辦法單獨跑 因為根目錄錯了，可能從app呼叫跑得動，最下面的註解(mock_data.py是一樣的)是可以跑的範例
from db.database import db
from models.group import Group

def calculate(group:Group):
    """
    根據 group_name 從資料庫取得 Group，計算並回傳 balances。
    balances 格式: {user_id: float}
    找不到 group 回傳空 dict。
    """
    

    balances = {user.id: 0.0 for user in group.members}

    for expense in group.expenses:
        amount = float(expense.amount)
        num_participants = len(expense.participants)
        share = round(amount / num_participants, 2)

        balances[expense.payer.id] += amount

        for user in expense.participants:
            balances[user.id] -= share

    # 將金額四捨五入保留兩位小數
    balances = {uid: round(balance, 2) for uid, balance in balances.items()}

    return balances

# import os
# import sys


# # 將專案根目錄加入 path，讓 import 正常運作
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from flask import Flask
# from db.database import init_db,db
# from models.user import User
# from services.calculation import calculate
# from services.settlement import settle

# if __name__ == '__main__':
#     app = Flask(__name__)
#     init_db(app)

#     with app.app_context():
#         # 指定要測試的群組名稱
#         group_name = 'Test Group 1'

#         # 計算金額結餘
#         balances = calculate(group_name)
#         print(f"[Balances for '{group_name}']")
#         for uid, amount in balances.items():
#             user = db.session.get(User, uid)
#             print(f"{user.name}: {amount}")

#         # 根據結餘進行結算轉帳
#         transactions = settle(balances)
#         print(f"\n[Transactions to settle up]")
#         for from_uid, to_uid, amount in transactions:
#             from_user = db.session.get(User, from_uid)
#             to_user = db.session.get(User, to_uid)

#             print(f"{from_user.name} pays {to_user.name}: {amount}")
