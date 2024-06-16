from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # Implementasi untuk mengambil profil user
    return jsonify({"message": "User profile"})
