"""
Expense object:
{
    "id": int
    "name": str
    "amount": float
    "note": str | None
    "created_at": Datetime  # to_dict() 會轉成 ISO 8601 格式的 str e.g. "2025-05-13T18:30:00"
    "payer": User
    "participants": list (each element is a Expense object)
    "group": Group
}

expense db 使用方式
0. import
from db.database import db
from models.expense import Expense

1. 新增 expense:
# 傳入 name, amount, note(optional), created_at, payer, group, participants 新增一個 Expense object
expense = Expense(
    name='Dinner',
    amount=150.0,
    note='dinner expense',
    created_at=datetime.fromisoformat('2025-05-13T18:30:00')
    payer=user1,
    group=group1,
    participants=[user1, user2]
)
db.session.add(expense)  # 將新支出加入到資料庫
db.session.commit()  # 提交變更

2. 根據 id 查詢 expense data:
expense = Expense.query.get(expense_id)  # return a Expense object -> 可以進一步利用 .id/.name/.amount/.note/.created_at/.payer/.group/.participants 取得其 instance variables

3. 修改 expense:
expense = Expense.query.get(expense_id)  # 先根據 id 找到要修改的 expense
expense.name = 'Updated Dinner'
expense.amount = 200.0
expense.note = 'updated note'
expense.create_at = datetime.fromisoformat('2025-05-13T18:30:00')
expense.payer = user3  # 可替換為其他 User object
expense.group = group1  # 可替換為其他 Group object
expense.participants = [user1, user3]  # 可替換為其他 User object
db.session.commit()  # 提交變更

4. 移除 expense:
expense = Expense.query.get(expense_id)  # 先根據 id 找到要移除的 expense
db.session.delete(expense)  # 從 session 中刪除
db.session.commit()  # 提交變更
"""

from db.database import db, expense_participants

class Expense(db.Model):
    __tablename__ = 'expenses_table'

    id = db.Column(db.Integer, primary_key=True)  # id: int, primary key(自動生成)
    name = db.Column(db.String(80), nullable=False)  # name: str(length <= 80), 必填
    amount = db.Column(db.Float, nullable=False)  # amount: float，必填
    note = db.Column(db.String(255), nullable=True)  # note: str(length <= 80) | None, 非必填
    created_at = db.Column(db.DateTime, nullable=False)  # created_at: Datetime, 必填

    # 多對一關聯：此 Expense 由哪個 User 付款
    payer_id = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    payer = db.relationship('User')  # 單向關聯到 User, 不能透過 User object access expense

    # 多對多關聯：此 Expense 由哪些 participants 分攤
    participants = db.relationship('User', secondary=expense_participants)  # 單向關聯到 User, 不能透過 User object access expense

    # 多對一關聯：此 Expense 屬於哪個 Group
    group_id = db.Column(db.Integer, db.ForeignKey('groups_table.id'), nullable=False)
    group = db.relationship('Group', back_populates='expenses')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "note": self.note,
            "created_at": self.created_at.isoformat(),  # 轉成 ISO 8601 格式的 str e.g. "2025-05-13T18:30:00"
            "payer": {
                "id": self.payer.id,
                "name": self.payer.name
            },
            "participants": [
                {"id": user.id, "name": user.name} for user in self.participants
            ],
            "group": {
                "id": self.group.id,
                "name": self.group.name
            }
        }

    def __repr__(self):
        user_names = [u.name for u in self.participants]
        return f"<Expense id={self.id}, name={self.name}, amount={self.amount}, note={self.note}, created_at={self.created_at}, payer={self.payer.name}, participants={user_names}, group={self.group.name}>"
