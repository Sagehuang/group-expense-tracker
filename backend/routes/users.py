from flask import Blueprint, request, jsonify
from db.database import db
from models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

# 使用者登入（若不存在則自動註冊）
# 根據 name 查詢使用者，若無則新增；最後回傳使用者資訊
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

    return jsonify({"id": user.id, "name": user.name}), 200

# 取得所有使用者及其所屬群組
@users_bp.route("/get_users", methods = ["GET"])
def get_users():
    users = User.query.all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "groups": [g.name for g in user.groups]  # Optional: list group names
        })

    return jsonify(result), 200

# 根據名稱刪除使用者
@users_bp.route("/delete_user", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    name = data.get("name")  # or use "id" if preferred

    user = User.query.filter_by(name=name).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User '{name}' deleted successfully."}), 200



""" Optional but useful additions later:
Add a /get_user/<id> route to get a single user

Support deleting users by id instead of just name

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
