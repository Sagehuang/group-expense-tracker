from flask import Blueprint, request, jsonify
from db.database import db
from models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

"""
這裡寫了根據 API 文件開發的前兩個 route, 並附上如何測試

# 範例一
@users_bp.route("/signin", methods=["POST"])
def sign_in():
    data = request.get_json()
    name = data.get("name")

    # 嘗試找出是否已有此使用者
    user = User.query.filter_by(name=name).first() # 若已有此使用者 return user object; 若無此使用者 return None

    # 若無此使用者，則新增此使用者
    if not user:
        user = User(name=name)  # 新增一個 User object
        db.session.add(user)  # 將新使用者加入到資料庫
        db.session.commit()  # 提交更改到資料庫

    return jsonify(user.to_dict()), 200

測試:
backend app run 起來的情況下另外開一個 terminal
curl -X POST http://localhost:5001/api/users/signin \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice"}'
terminal 會印出 backend app 的 response

# 範例二
@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user_detail(user_id):  # 上面用 <> 包起來的東西可以作為參數傳進函數裡
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user.to_dict()), 200

測試:
curl -X GET http://localhost:5001/api/users/1
"""

# 登入/註冊 user
@users_bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing name"}), 400

    user = User.query.filter_by(name=name).first()
    if not user:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    return jsonify(user.to_dict()), 200

# 根據 id 查詢 user 資料
@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user_detail(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# 根據 id 移除 user:
@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
