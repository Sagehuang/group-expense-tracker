from flask import Blueprint, request, jsonify
from db.database import db
from models.user import User
from models.group import Group

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

# 使用者註冊 / 登入
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

# 根據 id 查詢 user
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

# 根據 name 查詢 user data (models.user 那邊註解開的函數)
@users_bp.route("/get_user", methods=["POST"])
def get_user_by_name():
    data = request.get_json()
    name = data.get("name")
    user = User.query.filter_by(name=name).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# 新增 user 的 group (models.user 那邊註解開的函數)
@users_bp.route("/add_user_to_group", methods=["POST"])
def add_user_to_group():
    data = request.get_json()
    user_name = data.get("user_name")
    group_id = data.get("group_id")

    user = User.query.filter_by(name=user_name).first()
    group = Group.query.get(group_id)

    if not user or not group:
        return jsonify({"error": "User or group not found"}), 404

    if group not in user.groups:
        user.groups.append(group)
        db.session.commit()

    return jsonify({"message": f"User '{user.name}' added to group '{group.name}'"}), 200


""" Optional but useful additions later:

Support adding and deleting users by id instead of just name

Add input validation (e.g., ensure name is not empty) """



""" # 模擬一個使用者清單當作暫時的資料庫 -> 這裡最好搭配 class 寫，這裡是 bad example
fake_user_db = [
    {"name": "Alice", "group": ["A", "B", "C"]},
    {"name": "Bob", "group": ["A", "B"]}
]

@users_bp.route("/signin", methods=["POST"])
def sign_in():
    print("Received request headers:", dict(request.headers))  # debug
    print("Received request method:", request.method)  # debug
    
    if not request.is_json:
        print("Request is not JSON")  # debug
        return jsonify({"error": "Content-Type must be application/json"}), 400
        
    data = request.get_json()
    print("Received request data:", data)  # debug
    
    if not data or "name" not in data:
        print("Missing name in request data")  # debug
        return jsonify({"error": "Missing 'name' in request body"}), 400
        
    name = data.get("name")
    if not name:
        print("Name is empty")  # debug
        return jsonify({"error": "Name cannot be empty"}), 400

    # 嘗試找出是否已有此使用者
    match = [u for u in fake_user_db if u["name"] == name]
    user = match[0] if match else None

    # 若無此使用者，則新增一筆
    if not user:
        user = {"name": name, "group": []}
        fake_user_db.append(user)

    print("Returning user:", user)  # debug
    return jsonify(user), 200  # 用 json 格式回傳 user dict, 回傳 HTTP status code 200 (表示成功) """
