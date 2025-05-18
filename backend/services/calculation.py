"""
calculate_balance() 使用方式:
from services.calculation import calculate_balance

group = Group.query.get(group_id)
group_user_balances = calculate_balance(group)
print(group_user_balances)  # {2: -150.0, 3: 150.0} -> 代表 id = 2 的 user 應付 150.0, id = 3 的 user 應收 150.0
"""


def calculate_balance(group):
    """
    計算 group 中每個 user 的結餘，回傳 group_user_balances dict

    parameters:
    - group (Group): a group object

    return:
    - group_user_balances (dict): key 是 user id，value 是每個人的應收應付總額(float)，正為應收 / 負為應付
    """
    # 初始化每位成員的餘額為 0.0
    group_user_balances = {user.id: 0.0 for user in group.members}

    # 逐筆處理每一筆支出紀錄
    for expense in group.expenses:
        amount = float(expense.amount)                # 支出總金額
        num_participants = len(expense.participants)  # 分帳人數
        share = round(amount / num_participants, 2)   # 每人應分攤金額（平均分配，四捨五入至小數點後兩位）

        # 付款人先增加全額金額
        group_user_balances[expense.payer.id] += amount

        # 所有參與者（包括付款人自己）扣除應分攤金額
        for user in expense.participants:
            group_user_balances[user.id] -= share

    # 將所有餘額四捨五入至小數點後兩位，避免浮點誤差
    group_user_balances = {uid: round(balance, 2) for uid, balance in group_user_balances.items()}

    return group_user_balances
