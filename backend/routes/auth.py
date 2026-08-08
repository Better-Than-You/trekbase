import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from db.models import db, User, Staff

load_dotenv()
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@trekbase.com')

auth_bp = Blueprint('auth', __name__)

# given details creates tokens and returns it
def auth_response(entity_dict, role):
    tokens = {
        'identity': str(entity_dict['id']),
        'additional_claims': {'role': role, 'email': entity_dict['email']},
    }
    entity_dict['role'] = role
    return {
        'user': entity_dict,
        'access_token': create_access_token(**tokens),
        'refresh_token': create_refresh_token(**tokens),
    }


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

    # tokens create
    payload = auth_response(user.to_dict(), 'user')
    return jsonify({'message': 'User created successfully', **payload}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        if user.is_blacklisted: # BLACKLIST CHECK HERE < -----------------------------------
            return jsonify({'error': 'Account is blacklisted'}), 403
        role = 'admin' if email == ADMIN_EMAIL else 'user'
        return jsonify(auth_response(user.to_dict(), role)), 200

    staff = Staff.query.filter_by(email=email).first()
    if staff and staff.password_hash and staff.check_password(password):
        if staff.is_blacklisted: # BLACKLIST CHECK HERE < -----------------------------------
            return jsonify({'error': 'Account is blacklisted'}), 403
        return jsonify(auth_response(staff.to_dict(), 'staff')), 200

    return jsonify({'error': 'Invalid email or password'}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # basically renews the access token
    claims = get_jwt()
    access_token = create_access_token(
        identity=str(get_jwt_identity()),
        additional_claims={'role': claims.get('role'), 'email': claims.get('email')},
    )
    return jsonify({'access_token': access_token}), 200
