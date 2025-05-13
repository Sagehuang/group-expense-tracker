from flask import Blueprint, request, jsonify
from db.database import db
from models.expense import Expense
from models.group import Group
from models.user import User
from datetime import datetime

expense_bp = Blueprint("expenses", __name__, url_prefix="/api/expenses")

# 新增 expense:
@expense_bp.route("", methods=["POST"])
def create_expense():
    data = request.get_json()

    group_id = data.get("group_id")
    payer_id = data.get("payer_id")
    amount = data.get("amount")
    name = data.get("name")
    note = data.get("note")
    participant_ids = data.get("participant_ids")
    created_at = datetime.now()  # 可讓後端決定時間

    # 欄位驗證
    if not all([group_id, payer_id, name, amount, participant_ids]):
        return jsonify({"error": "Missing required fields"}), 400

    group = Group.query.get(group_id)
    payer = User.query.get(payer_id)

    if not group or not payer:
        return jsonify({"error": "Invalid group or payer"}), 404

    participants = [
        User.query.get(uid) for uid in participant_ids if User.query.get(uid)
    ]

    expense = Expense(
        name=name,
        amount=amount,
        note=note,
        created_at=created_at,
        payer=payer,
        group=group,
        participants=participants
    )
    db.session.add(expense)
    db.session.commit()

    return jsonify(expense.to_dict()), 201

# 根據 id 查詢 expense data:
@expense_bp.route("/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify(expense.to_dict()), 200

# 修改 expense:
@expense_bp.route("/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    data = request.get_json()

    # 基本欄位更新
    expense.name = data.get("name", expense.name)
    expense.amount = data.get("amount", expense.amount)
    expense.note = data.get("note", expense.note)

    # 更新 payer
    payer_id = data.get("payer_id")
    if payer_id:
        payer = User.query.get(payer_id)
        if not payer:
            return jsonify({"error": "Payer not found"}), 404
        expense.payer = payer

    # 更新 participants
    if "participant_ids" in data:
        participant_ids = data.get("participant_ids")
        participants = [
            User.query.get(uid) for uid in participant_ids if User.query.get(uid)
        ]
        expense.participants = participants

    db.session.commit()
    return jsonify(expense.to_dict()), 200


# 移除 expense:
@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": f"Expense {expense.id} deleted successfully."}), 200
