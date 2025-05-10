def settlement(balances):
    """
    根據每個使用者的結餘計算最少的轉帳組合。
    balances: dict {user_id: balance}
        - balance > 0 表示該使用者需收錢（債權人）
        - balance < 0 表示該使用者需還錢（債務人）
    return: list of (from_user_id, to_user_id, amount)
        - 每筆交易格式為：(債務人, 債權人, 金額)
    """

    # 將債權人與債務人分開：
    # - creditors: [[user_id, 應收金額]]
    # - debtors:   [[user_id, 應付金額（正數）]]
    creditors = []
    debtors = []

    for uid, bal in balances.items():
        if round(bal, 2) > 0:
            creditors.append([uid, round(bal, 2)])
        elif round(bal, 2) < 0:
            debtors.append([uid, round(-bal, 2)])  # 將負值轉為正數處理

    transactions = []  # 儲存最後的轉帳結果

    # 雙指標方式走訪債務人與債權人清單
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor_id, debt = debtors[i]
        creditor_id, credit = creditors[j]

        # 本輪的還款金額為債務與債權中的較小值
        amount = min(debt, credit)

        # 加入一筆還款紀錄：債務人付錢給債權人
        transactions.append((debtor_id, creditor_id, round(amount, 2)))

        # 更新債務與債權數值
        debtors[i][1] -= amount
        creditors[j][1] -= amount

        # 如果某債務人已還清，移動到下一位
        if debtors[i][1] == 0:
            i += 1

        # 如果某債權人已收滿，移動到下一位
        if creditors[j][1] == 0:
            j += 1

    return transactions  # 回傳最少轉帳路徑（可能不唯一）
