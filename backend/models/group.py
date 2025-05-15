"""
Group object:
{
    "id": int
    "name": str
    "members": list (each element is a User object)
    "expenses": list (each element is a Expense object)
}

group db 使用方式
0. import
from db.database import db
from models.group import Group

1. 新增 group:
group = Group(name=name)  # 傳入 name 新增一個 Group object
db.session.add(group)  # 將新群組加入到資料庫
db.session.commit()  # 提交變更

2. 根據 id 查詢 group data:
group = Group.query.get(group_id)  # return a Group object -> 可以進一步利用 .id/.name/.members/.expenses 取得其 instance variables

3. 新增 group 的 members
group = Group.query.get(group_id)  # 先根據 id 找到要新增 member 的 group
group.members.append(user)  # user 要是已經建立寫入資料庫的 User object
db.session.commit()  # 提交變更
# 注意：透過這個方法新增 group 的 member 後，對應的 User object 那邊也會自動在 groups 處新增這個 group (很方便，只要改一處另一處會自己改)

4. 移除 group:
group = Group.query.get(group_id)  # 先根據 id 找到要刪除的 group
db.session.delete(group)  # 從 session 中刪除
db.session.commit()  # 提交變更
"""

from db.database import db, user_groups

class Group(db.Model):
    __tablename__ = 'groups_table'

    id = db.Column(db.Integer, primary_key=True)  # id: int, primary key(自動生成)
    name = db.Column(db.String(80), nullable=False)  # name: str(length <= 80), 必填

    # 多對多關聯：此 Group 有哪些 User
    members = db.relationship('User', secondary=user_groups, back_populates='groups')

    # 一對多關聯：此 Group 有多筆 Expense
    expenses = db.relationship('Expense', back_populates='group', cascade='all, delete-orphan')  # 刪除 Group 時會自動刪除其所有 Expense

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "members": [
                {"id": user.id, "name": user.name} for user in self.members
            ],
            "expenses": [
                {"id": expense.id, "name": expense.name} for expense in self.expenses
            ]
        }

    def __repr__(self):
        user_names = [u.name for u in self.members]
        expense_names = [e.name for e in self.expenses]
        return f"<Group id={self.id}, name={self.name}, members={user_names}, expenses={expense_names}>"
