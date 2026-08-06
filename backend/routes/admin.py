from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from db.models import db, User, Staff, Trek, Booking
from datetime import datetime
import os 

admin_bp = Blueprint('admin', __name__)

# helper to parse date string into a date object
def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

# helper function to format the booking details and give custom object
def booking_with_details(booking):
    trek = db.session.get(Trek, booking.trek_id)
    user = db.session.get(User, booking.user_id)
    return {
        'id': booking.id,
        'status': booking.status,
        'booking_date': str(booking.booking_date),
        'trek': trek.to_dict() if trek else None,
        'user': user.to_dict() if user else None,
    }


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    bookings = [booking_with_details(b) for b in Booking.query.all()]
    staff = [s.to_dict() for s in Staff.query.all()]
    users = [u.to_dict() for u in User.query.all() if u.email != os.getenv('ADMIN_EMAIL', '')]

    treks = []
    for t in Trek.query.all():
        d = t.to_dict()
        staff_obj = db.session.get(Staff, t.assigned_staff_id)
        d['assigned_staff'] = staff_obj.to_dict() if staff_obj else None
        d['bookings_count'] = Booking.query.filter_by(trek_id=t.id).count()
        treks.append(d)

    return jsonify({
        'counts': {
            'bookings': len(bookings),
            'staff': len(staff),
            'users': len(users),
            'treks': len(treks),
        },
        'bookings': bookings,
        'staff': staff,
        'users': users,
        'treks': treks,
    }), 200 
    # working verified with postman


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    users = []
    for u in User.query.all():
        if u.email == os.getenv('ADMIN_EMAIL', ''):
            continue
        d = u.to_dict()
        d['bookings_count'] = Booking.query.filter_by(user_id=u.id).count()
        d['created_at'] = str(u.created_at) if u.created_at else None
        users.append(d)
    return jsonify({'users': users}), 200


@admin_bp.route('/users', methods=['POST'])
@jwt_required()
def add_user():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    name = (data.get('name') or '').strip()

    if not email or not password or not name:
        return jsonify({'error': 'Name, email and password are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added', 'user': user.to_dict()}), 201


@admin_bp.route('/staff', methods=['GET'])
@jwt_required()
def list_staff():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    staff = []
    for s in Staff.query.all():
        d = s.to_dict()
        d['assigned_treks'] = [t.to_dict() for t in Trek.query.filter_by(assigned_staff_id=s.id).all()]
        staff.append(d)
    return jsonify({'staff': staff}), 200


@admin_bp.route('/staff', methods=['POST'])
@jwt_required()
def add_staff():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json()
    name = (data.get('name') or '').strip()
    contact = (data.get('contact') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    staff = Staff(name=name, contact=contact, status='available')
    staff.email = email or None
    if password:
        staff.set_password(password)
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Staff added', 'staff': staff.to_dict()}), 201


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def user_details(user_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    d = user.to_dict()
    d['created_at'] = str(user.created_at) if user.created_at else None
    d['bookings'] = [booking_with_details(b) for b in Booking.query.filter_by(user_id=user.id).all()]
    return jsonify({'user': d}), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if user.email == os.getenv('ADMIN_EMAIL', ''):
        return jsonify({'error': 'Cannot delete admin account'}), 400

    Booking.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@admin_bp.route('/staff/<int:staff_id>', methods=['GET'])
@jwt_required()
def staff_details(staff_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    staff = db.session.get(Staff, staff_id)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404

    d = staff.to_dict()
    d['assigned_treks'] = [t.to_dict() for t in Trek.query.filter_by(assigned_staff_id=staff.id).all()]
    return jsonify({'staff': d}), 200


@admin_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
@jwt_required()
def delete_staff(staff_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    staff = db.session.get(Staff, staff_id)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404

    Trek.query.filter_by(assigned_staff_id=staff.id).update({'assigned_staff_id': None})
    db.session.delete(staff)
    db.session.commit()
    return jsonify({'message': 'Staff deleted'}), 200


@admin_bp.route('/treks', methods=['GET'])
@jwt_required()
def list_treks():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    treks = []
    for t in Trek.query.all():
        d = t.to_dict()
        staff = db.session.get(Staff, t.assigned_staff_id)
        d['assigned_staff'] = staff.to_dict() if staff else None
        d['bookings_count'] = Booking.query.filter_by(trek_id=t.id).count()
        treks.append(d)
    return jsonify({'treks': treks}), 200


@admin_bp.route('/treks', methods=['POST'])
@jwt_required()
def add_trek():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    location = (data.get('location') or '').strip()
    difficulty = (data.get('difficulty') or '').strip()
    status = (data.get('status') or 'pending').strip()

    if not name or not location or not difficulty:
        return jsonify({'error': 'Name, location and difficulty are required'}), 400
    if difficulty not in ('easy', 'moderate', 'hard'):
        return jsonify({'error': 'Difficulty must be easy, moderate or hard'}), 400
    if status not in ('pending', 'approved', 'open', 'closed', 'completed'):
        return jsonify({'error': 'Invalid trek status'}), 400

    trek = Trek(
        name=name,
        location=location,
        difficulty=difficulty,
        duration_days=int(data.get('duration_days') or 0),
        available_slots=int(data.get('available_slots') or 0),
        assigned_staff_id=data.get('assigned_staff_id') or None,
        status=status,
        start_date=parse_date(data.get('start_date')),
        end_date=parse_date(data.get('end_date')),
    )
    db.session.add(trek)
    db.session.commit()
    return jsonify({'message': 'Trek added', 'trek': trek.to_dict()}), 201


@admin_bp.route('/treks/<int:trek_id>', methods=['GET'])
@jwt_required()
def trek_details(trek_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    d = trek.to_dict()
    staff = db.session.get(Staff, trek.assigned_staff_id)
    d['assigned_staff'] = staff.to_dict() if staff else None
    d['bookings'] = [booking_with_details(b) for b in Booking.query.filter_by(trek_id=trek.id).all()]
    return jsonify({'trek': d}), 200


@admin_bp.route('/treks/<int:trek_id>', methods=['DELETE'])
@jwt_required()
def delete_trek(trek_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    Booking.query.filter_by(trek_id=trek.id).delete()
    db.session.delete(trek)
    db.session.commit()
    return jsonify({'message': 'Trek deleted'}), 200

