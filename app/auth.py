from flask import Blueprint, jsonify
from flask_login import logout_user, login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "User logged out successfully"})