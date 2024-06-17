from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_services import get_profile, forgot_password_user, reset_password_view_user, reset_password_user

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # Implementasi untuk mengambil profil user
    current_user = get_jwt_identity()
    return get_profile(current_user)

@bp.route('/forgot-password', methods=['POST'])
def forgot_password_endpoint():
    data = request.get_json()
    print(data)
    return forgot_password_user(data)

@bp.route('/reset-password-view/<token>', methods=['GET'])
def reset_password_view(token):
    return reset_password_view_user(token)

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")
    email = request.form.get("email")
    return reset_password_user(password, confirm_password, email)

@bp.route('/')

