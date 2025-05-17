import os
import sys

#  將專案根目錄加入系統模組搜尋路徑，讓 import 指令能順利導入上層的模組
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from db.database import init_db, db
from models.user import User
from services.calculation import calculate_balance  # 用來計算每位成員的金額結餘
from services.settlement import settle_up          # 用來計算成員間轉帳的方式
from models.group import Group                     # 群組的資料模型

def main():
    # 初始化 Flask 應用
    app = Flask(__name__)
    init_db(app)  # 初始化資料庫（連接、設定等）

    # 建立 Flask 應用上下文，才能使用 db.session 與 ORM 功能
    with app.app_context():
        # 取得 id 為 2 的群組資料（這是你要測試的群組）
        group = Group.query.get(2)

        # 若查不到該群組，直接結束程式
        if not group:
            return

        #  計算該群組中每位成員的結餘（正值代表該收錢，負值代表該付錢）
        balances = calculate_balance(group)
        print(f"[Balances for '{group.name}']")

        # 將每位成員的結餘印出
        for uid, amount in balances.items():
            user = db.session.get(User, uid)  # 根據 user id 查出對應的使用者物件
            print(f"{user.name}: {amount}")   # 印出使用者名稱與其結餘

        #  根據 balances 計算誰應該付錢給誰，讓所有人結清帳款
        transactions = settle_up(balances)
        print(f"\n[Transactions to settle up]")

        # 印出每一筆轉帳紀錄
        for from_uid, to_uid, amount in transactions:
            from_user = db.session.get(User, from_uid)
            to_user = db.session.get(User, to_uid)
            print(f"{from_user.name} pays {to_user.name}: {amount}")

# 當此檔案被直接執行時，會呼叫 main()
if __name__ == '__main__':
    main()
