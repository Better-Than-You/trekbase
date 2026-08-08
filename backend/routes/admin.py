from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from db.models import db, User, Staff, Trek, Booking
from datetime import datetime
import os
import json
from cache import cache_get, cache_set, invalidate_treks

admin_bp = Blueprint('admin', __name__)

# date to yyyy-mm-dd string helper
def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


# booking details parser
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


# trek > trek + booking count + staff
def serialize_trek(trek):
    d = trek.to_dict()
    staff = db.session.get(Staff, trek.assigned_staff_id)
    d['assigned_staff'] = staff.to_dict() if staff else None
    d['bookings_count'] = Booking.query.filter_by(trek_id=trek.id).count()
    return d


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    bookings = [booking_with_details(b) for b in Booking.query.all()]
    staff = [s.to_dict() for s in Staff.query.all()]
    users = [u.to_dict() for u in User.query.all() if u.email != os.getenv('ADMIN_EMAIL', '')]
    treks = [serialize_trek(t) for t in Trek.query.all()]

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

# ------ users ----------------
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    
    q = (request.args.get('q') or '').strip().lower()
    query = User.query
    if q:
        # search by name/email
        query = query.filter(db.or_(User.name.ilike(f'%{q}%'), User.email.ilike(f'%{q}%')))

    users = []
    for u in query.all():
        # exclude the admin
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
    address = (data.get('address') or '').strip()
    pin = (data.get('pin') or '').strip()
    phone = (data.get('phone') or '').strip() or None

    if not email or not password or not name:
        return jsonify({'error': 'Name, email and password are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    # ensuring unique phone num
    if phone and User.query.filter_by(phone=phone).first():
        return jsonify({'error': 'Phone number already registered'}), 409

    user = User(email=email, name=name, address=address or None, pin=pin or None, phone=phone)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added', 'user': user.to_dict()}), 201

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


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    address = (data.get('address') or '').strip()
    pin = (data.get('pin') or '').strip()
    phone = (data.get('phone') or '').strip() or None

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    existing = User.query.filter(User.email == email, User.id != user_id).first()
    if existing:
        return jsonify({'error': 'Email already registered'}), 409

    if phone:
        phone_taken = User.query.filter(User.phone == phone, User.id != user_id).first()
        if phone_taken:
            return jsonify({'error': 'Phone number already registered'}), 409

    user.name = name
    user.email = email
    user.address = address or None
    user.pin = pin or None
    user.phone = phone
    db.session.commit()
    return jsonify({'message': 'User updated', 'user': user.to_dict()}), 200


@admin_bp.route('/users/<int:user_id>/blacklist', methods=['PUT'])
@jwt_required()
def toggle_user_blacklist(user_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # can't blacklist admin
    if user.email == os.getenv('ADMIN_EMAIL', ''):
        return jsonify({'error': 'Cannot blacklist the admin account'}), 400

    user.is_blacklisted = bool((request.get_json() or {}).get('is_blacklisted'))
    db.session.commit()
    return jsonify({'message': 'User updated', 'user': user.to_dict()}), 200


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


# ------------ staffs ---------------
@admin_bp.route('/staff', methods=['GET'])
@jwt_required()
def list_staff():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    
    q = (request.args.get('q') or '').strip().lower()
    query = Staff.query
    if q:
        # search by name/email/contact
        query = query.filter(db.or_(
            Staff.name.ilike(f'%{q}%'),
            Staff.email.ilike(f'%{q}%'),
            Staff.contact.ilike(f'%{q}%'),
        ))

    staff = []
    for s in query.all():
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


@admin_bp.route('/staff/<int:staff_id>', methods=['PUT'])
@jwt_required()
def edit_staff(staff_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    staff = db.session.get(Staff, staff_id)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404

    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    contact = (data.get('contact') or '').strip()
    email = (data.get('email') or '').strip().lower()
    status = (data.get('status') or '').strip()

    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if status and status not in ('available', 'assigned', 'not_available'):
        return jsonify({'error': 'Status must be available, assigned or not_available'}), 400

    if email:
        existing = Staff.query.filter(Staff.email == email, Staff.id != staff_id).first()
        if existing:
            return jsonify({'error': 'Email already registered'}), 409

    staff.name = name
    staff.contact = contact or None
    staff.email = email or None
    if status:
        staff.status = status
    db.session.commit()
    return jsonify({'message': 'Staff updated', 'staff': staff.to_dict()}), 200


@admin_bp.route('/staff/<int:staff_id>/blacklist', methods=['PUT'])
@jwt_required()
def toggle_staff_blacklist(staff_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    staff = db.session.get(Staff, staff_id)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404

    staff.is_blacklisted = bool((request.get_json() or {}).get('is_blacklisted'))
    db.session.commit()
    return jsonify({'message': 'Staff updated', 'staff': staff.to_dict()}), 200


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

# --------------- treks ----------------------
@admin_bp.route('/treks', methods=['GET'])
@jwt_required()
def list_treks():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    q = (request.args.get('q') or '').strip().lower()
    key = f"treks:all:{q}" if q else 'treks:all'
    cached = cache_get(key)
    if cached is not None:
        return jsonify(json.loads(cached)), 200
    query = Trek.query
    if q:
        query = query.filter(db.or_(Trek.name.ilike(f'%{q}%'), Trek.location.ilike(f'%{q}%')))
    data = {'treks': [serialize_trek(t) for t in query.all()]}
    cache_set(key, json.dumps(data))
    return jsonify(data), 200


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
    invalidate_treks()
    return jsonify({'message': 'Trek added', 'trek': trek.to_dict()}), 201


@admin_bp.route('/treks/<int:trek_id>', methods=['GET'])
@jwt_required()
def trek_details(trek_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    key = f'trek:{trek_id}'
    cached = cache_get(key)
    if cached is not None:
        return jsonify(json.loads(cached)), 200
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    d = serialize_trek(trek)
    d['bookings'] = [booking_with_details(b) for b in Booking.query.filter_by(trek_id=trek.id).all()]
    data = {'trek': d}
    cache_set(key, json.dumps(data))
    return jsonify(data), 200


@admin_bp.route('/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
def edit_trek(trek_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404

    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    location = (data.get('location') or '').strip()
    difficulty = (data.get('difficulty') or '').strip()
    status = (data.get('status') or '').strip()

    if not name or not location or not difficulty:
        return jsonify({'error': 'Name, location and difficulty are required'}), 400
    if difficulty not in ('easy', 'moderate', 'hard'):
        return jsonify({'error': 'Difficulty must be easy, moderate or hard'}), 400
    if status not in ('pending', 'approved', 'open', 'closed', 'completed'):
        return jsonify({'error': 'Invalid trek status'}), 400

    trek.name = name
    trek.location = location
    trek.difficulty = difficulty
    trek.duration_days = int(data.get('duration_days') or 0)
    trek.available_slots = int(data.get('available_slots') or 0)
    trek.assigned_staff_id = data.get('assigned_staff_id') or None
    trek.status = status
    trek.start_date = parse_date(data.get('start_date'))
    trek.end_date = parse_date(data.get('end_date'))
    db.session.commit()
    invalidate_treks()
    return jsonify({'message': 'Trek updated', 'trek': trek.to_dict()}), 200


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
    invalidate_treks()
    return jsonify({'message': 'Trek deleted'}), 200


# ------------ manual triggers ------------------------------
@admin_bp.route('/jobs/reminders', methods=['POST'])
@jwt_required()
def trigger_reminders():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    from tasks import daily_trek_reminders
    result = daily_trek_reminders.delay()
    return jsonify({'message': 'Daily reminders triggered', 'task_id': result.id}), 202


@admin_bp.route('/jobs/monthly-report', methods=['POST'])
@jwt_required()
def trigger_monthly_report():
    if get_jwt().get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    from tasks import monthly_activity_report
    result = monthly_activity_report.delay()
    return jsonify({'message': 'Monthly report triggered', 'task_id': result.id}), 202

