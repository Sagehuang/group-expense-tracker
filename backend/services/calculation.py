#這個code沒有辦法單獨跑 因為根目錄錯了，可能從app呼叫跑得動，最下面的註解(mock_data.py是一樣的)是可以跑的範例
from db.database import db
from models.group import Group

def calculate_balance(group: Group):
    """
根據傳入的 Group 物件，計算並回傳 balances。
balances 格式: {user_id: float}
"""


    # 初始化每位成員的餘額為 0.0
    balances = {user.id: 0.0 for user in group.members}

    # 逐筆處理每一筆支出紀錄
    for expense in group.expenses:
        amount = float(expense.amount)               # 支出總金額
        num_participants = len(expense.participants) # 分帳人數
        share = round(amount / num_participants, 2)  # 每人應分攤金額（平均分配，四捨五入至小數點後兩位）

        # 付款人先增加全額金額
        balances[expense.payer.id] += amount

        # 所有參與者（包括付款人自己）扣除應分攤金額
        for user in expense.participants:
            balances[user.id] -= share

    # 將所有餘額四捨五入至小數點後兩位，避免浮點誤差
    balances = {uid: round(balance, 2) for uid, balance in balances.items()}

    return balances



