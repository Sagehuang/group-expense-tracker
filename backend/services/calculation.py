from decimal import Decimal, getcontext

# 設定 Decimal 小數運算的精度為 10 位數，避免浮點誤差
getcontext().prec = 10


def calculation(group):
    """
    計算群組中每位成員的最終結餘（誰該付錢、誰該收錢）。
    
    參數：
        group: Group 物件，包含成員與花費紀錄。
        
    回傳：
        balances: dict，{user_id: Decimal 金額}，金額 > 0 表示該使用者應收款，< 0 表示應付款。
    """

    # 初始化每位使用者的結餘為 0
    balances = {user.id: Decimal('0') for user in group.members}

    # 處理群組中的每筆花費
    for expense in group.expenses:
        # 將花費金額轉為 Decimal 類型
        amount = Decimal(str(expense.amount))
        
        # 計算每位參與者應分攤的金額
        share = amount / Decimal(len(expense.participants))
        
        # 拿到付款人的 ID
        payer_id = expense.payer.id

        # 付款人先支付全部金額，結餘加上 amount
        balances[payer_id] += amount

        # 每位參與者要付出他們的 share，所以減掉對應金額
        for user in expense.participants:
            balances[user.id] -= share

    # 將每位使用者的結餘四捨五入至小數點後兩位（可選步驟）
    balances = {uid: round(balance, 2) for uid, balance in balances.items()}

    return balances  # 回傳所有人的結餘結果
