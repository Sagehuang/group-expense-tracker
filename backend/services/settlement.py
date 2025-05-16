# from decimal import Decimal, ROUND_HALF_UP

# def settle_up(balances):
#     """
#     根據每位使用者的結餘計算最簡轉帳方式
#     balances: dict {user_id: Decimal 金額（正為應收，負為應付）}
#     return: list of (from_user_id, to_user_id, amount: Decimal)
#     """
#     # 拆分債權人與債務人
#     creditors = []
#     debtors = []

#     for uid, bal in balances.items():
#         if bal > 0:
#             creditors.append([uid, bal])
#         elif bal < 0:
#             debtors.append([uid, -bal])  # 債務轉為正數

#     transactions = []
#     i, j = 0, 0

#     while i < len(debtors) and j < len(creditors):
#         debtor_id, debt = debtors[i]
#         creditor_id, credit = creditors[j]
#         amount = min(debt, credit).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

#         transactions.append((debtor_id, creditor_id, amount))

#         debtors[i][1] -= amount
#         creditors[j][1] -= amount

#         if debtors[i][1] == Decimal('0'):
#             i += 1
#         if creditors[j][1] == Decimal('0'):
#             j += 1

#     return transactions

def settle(balances):
    """
    根據每位使用者的結餘計算最簡轉帳方式（使用 float）
    balances: dict {user_id: float 金額（正為應收，負為應付）}
    return: list of (from_user_id, to_user_id, amount: float)
    """
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
        amount = round(min(debt, credit), 2)

        transactions.append((debtor_id, creditor_id, amount))

        debtors[i][1] -= amount
        creditors[j][1] -= amount

        if round(debtors[i][1], 2) == 0:
            i += 1
        if round(creditors[j][1], 2) == 0:
            j += 1

    return transactions
