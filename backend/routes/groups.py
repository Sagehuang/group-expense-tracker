from flask import Blueprint, request, jsonify
from db.database import db
from models.group import Group
from models.user import User

group_bp = Blueprint("groups", __name__, url_prefix="/api/groups")

# 建立 group
@group_bp.route("", methods=["POST"])
def create_group():
    data = request.get_json()
    name = data.get("name")
    creator_id = data.get("creator_id")

    if not name or not creator_id:
        return jsonify({"error": "Missing group name or user_id"}), 400

    creator = User.query.get(creator_id)
    if not creator:
        return jsonify({"error": "User not found"}), 404

    group = Group(name=name)
    group.members.append(creator)  # 建立時順便加入創建者
    db.session.add(group)
    db.session.commit()

    return jsonify(group.to_dict()), 201

# 新增 group 的 members
@group_bp.route("/<int:group_id>/join", methods=["POST"])
def join_group(group_id):
    data = request.get_json()
    user_id = data.get("user_id")

    group = Group.query.get(group_id)
    user = User.query.get(user_id)

    if not group or not user:
        return jsonify({"error": "Group or user not found"}), 404

    if user not in group.members:
        group.members.append(user)
        db.session.commit()
    else:
        return jsonify({"error": f"User {user.name} already joined group {group.name}"}), 400

    return jsonify({"message": f"User {user.name} added to group {group.name}"}), 200

# 根據 group_id 查詢 group 資料
@group_bp.route("/<int:group_id>", methods=["GET"])
def get_group(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    return jsonify(group.to_dict()), 200

# 移除 group:
@group_bp.route("/<int:group_id>", methods=["DELETE"])
def delete_group(group_id):
    group = Group.query.get(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    db.session.delete(group)
    db.session.commit()
    return jsonify({"message": f"Group '{group.name}' deleted successfully."}), 200
