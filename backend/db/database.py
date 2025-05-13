from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 建立 SQLAlchemy 實例
db = SQLAlchemy()

def init_db(app):
    """初始化資料庫連接"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///group_expense_tracker.db'  # 使用 SQLite 資料庫，資料存在本機的 group_expense_tracker.db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 關閉預設自動追蹤物件變化的功能

    db.init_app(app)  # 綁定 Flask app 和 SQLAlchemy 的 db

    from models.user import User  # db debug
    from models.group import Group  # db debug
    from models.expense import Expense  # db debug

    with app.app_context():
        db.create_all()  # 根據使用 SQLAlchemy 定義的所有 data models，在資料庫中建立對應的表格

        # db testing
        if not User.query.first():  # 如果資料表是空的，才建立測試資料
            # 建立使用者
            user1 = User(name='Alice')
            user2 = User(name='Bob')
            user3 = User(name='Charlie')

            # 建立群組，包含上述使用者
            group1 = Group(name='Test Group 1', members=[user1, user2])
            group2 = Group(name='Test Group 2', members=[user2, user3])

            # 建立支出
            expense1 = Expense(
                name='Dinner',
                amount=150.0,
                note='Group 1 dinner expense',
                created_at=datetime.fromisoformat('2025-05-13T20:00:00'),
                payer=user1,
                group=group1,
                participants=[user1, user2]
            )

            expense2 = Expense(
                name='Hotel',
                amount=300.0,
                note='Group 2 hotel expense',
                created_at=datetime.fromisoformat('2025-05-13T15:30:00'),
                payer=user3,
                group=group2,
                participants=[user2, user3]
            )

            expense3 = Expense(
                name='Museum Tickets',
                amount=90.0,
                note=None,  # 可為 None
                created_at=datetime.fromisoformat('2025-05-13T09:00:00'),
                payer=user2,
                group=group1,
                participants=[user1, user2]
            )

            db.session.add_all([
                user1, user2, user3,
                group1, group2,
                expense1, expense2, expense3
            ])
            db.session.commit()

# association
# 定義 User 和 Group 的多對多關聯
user_groups = db.Table(
    'user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users_table.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups_table.id'), primary_key=True)
)

# 定義 Expense 和 User 的多對多關聯
expense_participants = db.Table(
    'expense_participants',
    db.Column('expense_id', db.Integer, db.ForeignKey('expenses_table.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users_table.id'), primary_key=True)
)
