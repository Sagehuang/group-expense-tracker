"""
settle_up() 使用方式:
from services.calculation import calculate_balance
from services.settlement import settle_up

group = Group.query.get(group_id)
group_user_balances = calculate_balance(group)  # 先透過 calculate_balance() 計算得到 group_user_balances
transactions = settle_up(group_user_balances)
print(transactions)  # [(2, 1, 130.0), (2, 3, 150.0)] -> 代表 user2 要給 user1 130.0, user2 要給 user3 150.0
"""


def settle_up(group_user_balances):
    """
    計算 group 中能結清款項的最短付款路徑

    parameters:
    - group_user_balances (dict): key 是 user id，value 是每個人的應收應付總額(float)，正為應收 / 負為應付 -> 此參數可由 calculate_balance() 計算而得

    return:
    - transactions (list): each element is a tuple that looks like (payer_id, receiver_id, amount)
    """
    # 建立兩個清單：分別儲存債權人（應收款）與債務人（應付款）
    creditors = []  # 格式：[user_id, 金額]
    debtors = []    # 格式：[user_id, 金額（轉為正數）]

    # 將 balances 字典中的正負金額分類
    for uid, bal in group_user_balances.items():
        if bal > 0:
            creditors.append([uid, bal])     # 將債權人加入清單
        elif bal < 0:
            debtors.append([uid, -bal])      # 債務轉為正數後加入清單

    transactions = []  # 儲存所有的轉帳交易 (債務人, 債權人, 金額)
    i, j = 0, 0         # i 用於走訪債務人清單，j 用於走訪債權人清單

    # 使用 greedy 的方式逐一配對債務人與債權人，直到一方清空
    while i < len(debtors) and j < len(creditors):
        debtor_id, debt = debtors[i]           # 當前債務人與其剩餘債務
        creditor_id, credit = creditors[j]     # 當前債權人與其剩餘應收金額

        # 計算此次轉帳金額，為兩者中較小者，取小數點後兩位
        amount = round(min(debt, credit), 2)

        # 建立轉帳紀錄：誰付錢給誰多少
        transactions.append((debtor_id, creditor_id, amount))

        # 更新剩餘債務與債權金額
        debtors[i][1] -= amount
        creditors[j][1] -= amount

        # 若債務已清償完畢，移動到下一個債務人
        if round(debtors[i][1], 2) == 0:
            i += 1
        # 若債權已收完，移動到下一個債權人
        if round(creditors[j][1], 2) == 0:
            j += 1

    # 回傳所有的轉帳紀錄
    return transactions


'''
amount 改用 Decimal 計算的寫法

from decimal import Decimal, ROUND_HALF_UP

def settle_up(balances):
    """
    根據每位使用者的結餘計算最簡轉帳方式
    balances: dict {user_id: Decimal 金額（正為應收，負為應付）}
    return: list of (from_user_id, to_user_id, amount: Decimal)
    """
    # 拆分債權人與債務人
    creditors = []
    debtors = []

    for uid, bal in balances.items():
        if bal > 0:
            creditors.append([uid, bal])
        elif bal < 0:
            debtors.append([uid, -bal])  # 債務轉為正數

    transactions = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor_id, debt = debtors[i]
        creditor_id, credit = creditors[j]
        amount = min(debt, credit).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        transactions.append((debtor_id, creditor_id, amount))

        debtors[i][1] -= amount
        creditors[j][1] -= amount

        if debtors[i][1] == Decimal('0'):
            i += 1
        if creditors[j][1] == Decimal('0'):
            j += 1

    return transactions

'''