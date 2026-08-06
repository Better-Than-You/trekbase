import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from db.models import db, User, Staff

load_dotenv()
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@trekbase.com')

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()

    if not email or not password or not name:
        return jsonify({'error': 'Email, password and name are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': 'user', 'email': user.email}
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={'role': 'user', 'email': user.email}
    )

    print(f'registered : {email}')
    user_dict = user.to_dict()
    user_dict['role'] = 'user'
    return jsonify({'message': 'User created successfully', 'user': user_dict, 'access_token': access_token, 'refresh_token': refresh_token}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # trekkers or admin
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        role = 'admin' if email == ADMIN_EMAIL else 'user'
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': role, 'email': user.email}
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims={'role': role, 'email': user.email}
        )
        user_dict = user.to_dict()
        user_dict['role'] = role
        print(f'login : {email} : {role}')
        return jsonify({'access_token': access_token, 'user': user_dict, 'refresh_token': refresh_token}), 200

    # staff
    staff = Staff.query.filter_by(email=email).first()
    if staff and staff.password_hash and staff.check_password(password):
        role = 'staff'
        access_token = create_access_token(
            identity=str(staff.id),
            additional_claims={'role': role, 'email': staff.email}
        )
        refresh_token = create_refresh_token(
            identity=str(staff.id),
            additional_claims={'role': role, 'email': staff.email}
        )
        staff_dict = staff.to_dict()
        staff_dict['role'] = role
        print(f'login : {email} : {role}')
        return jsonify({'access_token': access_token, 'user': staff_dict, 'refresh_token': refresh_token}), 200

    return jsonify({'error': 'Invalid email or password'}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200
