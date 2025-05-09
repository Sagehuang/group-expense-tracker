from flask import Flask, jsonify
from flask_cors import CORS
from routes.users import users_bp
# from routes.groups import groups_bp
# from routes.transactions import transactions_bp

def create_app():
    app = Flask(__name__)
    # CORS(app)  # 啟用 CORS 支援

    # 設定 CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:*", "http://127.0.0.1:*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    # 註冊 Blueprints
    app.register_blueprint(users_bp)
    # app.register_blueprint(groups_bp)
    # app.register_blueprint(transactions_bp)

    # 添加測試路由
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Backend is running!"}), 200

    # 其他初始化可加在這裡（例如 DB、CORS、config）
    # from db.database import init_db
    # init_db(app)

    return app

# 當這個檔案是被直接執行的，而不是被其他程式匯入使用時，才會執行這段區塊 -> 用於作爲 backend 的啟動入口
if __name__ == "__main__":
    app = create_app()
    print("Backend server starting on http://localhost:5001")  # debug
    app.run(host='0.0.0.0', port=5001, debug=True)
