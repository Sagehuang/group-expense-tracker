# 匯入結餘計算與最短付款路徑演算法
from calculation import calculation
from settlement import settlement


# === 使用者 User 類別 ===
class User:
    def __init__(self, id, name):
        self.id = id                  # 使用者唯一 ID（整數）
        self.name = name              # 使用者名稱
        self.groups = []              # 參與的群組列表（Group 物件）

    def join_group(self, group):
        # 加入群組：若未加入則加進使用者與群組雙方記錄
        if group not in self.groups:
            self.groups.append(group)
            group.add_member(self)


# === 群組 Group 類別 ===
class Group:
    def __init__(self, id, name):
        self.id = id                  # 群組 ID
        self.name = name              # 群組名稱
        self.members = []             # 群組成員（User 物件列表）
        self.expenses = []            # 群組內的花費紀錄（Expense 物件列表）

    def add_member(self, user):
        # 新增成員：支援單一使用者或使用者清單
        if type(user) == list:
            for u in user:
                self.add_member(u)
        else:
            if user not in self.members:
                self.members.append(user)

    def add_expense(self, expense):
        # 新增一筆花費紀錄
        self.expenses.append(expense)


# === 花費 Expense 類別 ===
class Expense:
    def __init__(self, name, amount, payer, participants, note=None):
        self.name = name                      # 花費名稱（例：午餐）
        self.amount = amount                  # 花費金額
        self.payer = payer                    # 付款人（User 物件）
        self.participants = participants      # 參與分攤的使用者列表
        self.note = note                      # 備註（可選）


# === 建立 Mock 測試資料 ===
exam_user = ["a", "b", "c"]       # 使用者名稱
exam_group = ["d", "e"]           # 群組名稱
exam_expense = ["f", "g"]         # 花費名稱（未使用）

# 初始化 User、Group、Expense 清單
users = []
groups = []
expenses = []

# 建立使用者實體
for i, j in enumerate(exam_user):
    users.append(User(i, j))

# 建立群組實體
for i, j in enumerate(exam_group):
    groups.append(Group(i, j))

# 將全部使用者加入第一個群組
groups[0].add_member(users)

# 建立兩筆花費：
# - 使用者 a 付 100 元，大家平分
# - 使用者 b 付 50 元，大家平分
expenses.append(Expense("money1", 720, users[0], users))
expenses.append(Expense("money2", 50, users[1], users))

# 將花費加入群組
for e in expenses:
    groups[0].add_expense(e)


# === 計算每位使用者的結餘 ===
balances = calculation(groups[0])

# 顯示每位使用者的結餘
for user in users:
    print(f"{user.name} 的結餘：{balances[user.id]}")


# === 計算最短轉帳方案 ===
transactions = settlement(balances)

# 顯示誰要付多少給誰
for frm, to, amt in transactions:
    print(f"{users[frm].name} 付 {amt} 元給 {users[to].name}")






