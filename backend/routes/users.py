from flask import Blueprint, request, jsonify
# from models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

# 模擬一個使用者清單當作暫時的資料庫 -> 這裡最好搭配 class 寫，這裡是 bad example
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
    return jsonify(user), 200  # 用 json 格式回傳 user dict, 回傳 HTTP status code 200 (表示成功)

"""
等到 db 完成後 route 應該會改寫成下面這樣，也就是不需要假資料的版本：
@users_bp.route("/signin", methods=["POST"])
def sign_in():
    data = request.get_json()
    name = data.get("name")

    # 這段先不用管，用途是跟資料庫互動 e.g. 取資料、存資料、更新資料，等到 models.user 寫好就知道怎麼用了，在此之前可以先用簡單的邏輯代替，如上
    user = User.query.filter_by(name=name).first()
    if not user:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    return jsonify({"id": user.id, "name": user.name}), 200
"""