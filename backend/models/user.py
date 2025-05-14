"""
User object:
{
    "id": int
    "name": str
    "groups": list (each element is a Group object)
}

user db 使用方式
0. import
from db.database import db
from models.user import User

1. 新增 user:
user = User(name=name)  # 傳入 name 新增一個 User object
db.session.add(user)  # 將新使用者加入到資料庫
db.session.commit()  # 提交變更

2. 根據 name / id 查詢 user data:
user = User.query.filter_by(name=name).first()  # return a User object -> 可以進一步利用 .id/.name/.groups 取得其 instance variables
user = User.query.get(user_id)  # return a User object -> 可以進一步利用 .id/.name/.groups 取得其 instance variables

3. 新增 user 的 group:
user = User.query.get(user_id)  # 先根據 id 找到要新增 group 的 user
user.groups.append(group)  # group 要是已經建立寫入資料庫的 Group object (也就是說必須在此之前先提交 db.session.commit() 細節見 models/group.py)
db.session.commit()  # 提交變更
# 注意：透過這個方法新增 user 的 group 後，對應的 Group object 那邊也會自動在 members 處新增這個 user (很方便，只要改一處另一處會自己改)

4. 移除 user:
user = User.query.get(user_id)  # 先根據 id 找到要刪除的 user
db.session.delete(user)  # 從 session 中刪除
db.session.commit()  # 提交變更
"""

from db.database import db, user_groups

class User(db.Model):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)  # id: int, primary key(自動生成)
    name = db.Column(db.String(80), nullable=False)  # name: str(length <= 80), 必填

    # 多對多關聯：此 User 參加哪些 Group
    groups = db.relationship('Group', secondary=user_groups, back_populates='members')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "groups": [
                {"id": group.id, "name": group.name} for group in self.groups
            ]
        }

    def __repr__(self):
        group_names = [g.name for g in self.groups]
        return f"<User id={self.id}, name={self.name}, groups={group_names}>"
