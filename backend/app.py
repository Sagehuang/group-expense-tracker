from flask import Flask, jsonify
from flask_cors import CORS
from db.database import db, init_db
from sqlalchemy import inspect  # db debug
from models.user import User  # db debug
from models.group import Group  # db debug
from models.expense import Expense  # db debug
from routes.users import users_bp
from routes.groups import group_bp
from routes.expenses import expense_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # 啟用 CORS

    init_db(app)  # 初始化資料庫

    # 設置 Blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(expense_bp)

    """
    route testing
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Backend is running!"}), 200
    """

    # db debug 方法：另外開一個 terminal 輸入 curl http://localhost:5001/show_users (/後面接下面你想要測試的東西)
    # db debug
    @app.route('/show_tables')
    def show_tables():
        # 列出所有資料表
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        return "\n".join(tables)
    
    # db debug
    @app.route('/show_users')
    def show_users():
        # 列出所有 User 資料
        users = User.query.all()
        return "\n".join([repr(user) for user in users])
    
    # db debug
    @app.route('/show_groups')
    def show_groups():
        # 列出所有 Group 資料
        groups = Group.query.all()
        return "\n".join([repr(group) for group in groups])
    
    # db debug
    @app.route('/show_expenses')
    def show_expenses():
        # 列出所有 Expense 資料
        expenses = Expense.query.all()
        return "\n".join([repr(expense) for expense in expenses])

    return app

# 當這個檔案是被直接執行的，而不是被其他程式匯入使用時，才會執行這段區塊 -> 用於作爲 backend 的啟動入口
if __name__ == "__main__":
    app = create_app()
    app.run(port=5001, debug=True)
