import os
import sys


# 將專案根目錄加入 path，讓 import 正常運作
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from db.database import init_db,db
from models.user import User
from services.calculation import calculate
from services.settlement import settle
from models.group import Group
def main():
    app = Flask(__name__)
    init_db(app)

    with app.app_context():
        # 指定要測試的群組名稱
        group_name = 'Test Group 1'
        group = Group.query.filter_by(name=group_name).first()
        if not group:
            return
        # 計算金額結餘
        balances = calculate(group)
        print(f"[Balances for '{group_name}']")
        for uid, amount in balances.items():
            user = db.session.get(User, uid)
            print(f"{user.name}: {amount}")

        # 根據結餘進行結算轉帳
        transactions = settle(balances)
        print(f"\n[Transactions to settle up]")
        for from_uid, to_uid, amount in transactions:
            from_user = db.session.get(User, from_uid)
            to_user = db.session.get(User, to_uid)

            print(f"{from_user.name} pays {to_user.name}: {amount}")

if __name__ == '__main__':
    main()
    