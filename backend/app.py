from flask import Flask, jsonify
from flask_cors import CORS
from routes.users import users_bp
# from routes.groups import groups_bp
# from routes.transactions import transactions_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # 啟用 CORS

    # 設置 Blueprints
    app.register_blueprint(users_bp)
    # app.register_blueprint(groups_bp)
    # app.register_blueprint(transactions_bp)

    # route testing
    # @app.route('/test', methods=['GET'])
    # def test():
    #     return jsonify({"message": "Backend is running!"}), 200

    return app

# 當這個檔案是被直接執行的，而不是被其他程式匯入使用時，才會執行這段區塊 -> 用於作爲 backend 的啟動入口
if __name__ == "__main__":
    app = create_app()
    app.run(port=5001, debug=True)
