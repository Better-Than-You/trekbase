from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from celery.result import AsyncResult
from celery_app import celery_app
from db.models import db, User, Trek, Booking
from datetime import datetime
import json
from cache import cache_get, cache_set, invalidate_treks

user_bp = Blueprint('user', __name__)


# # booking > id, status, date, user
def booking_with_trek(booking):
    trek = db.session.get(Trek, booking.trek_id)
    return {
        'id': booking.id,
        'status': booking.status,
        'booking_date': str(booking.booking_date),
        'trek': trek.to_dict() if trek else None,
    }


@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403

    user_id = int(get_jwt_identity())
    available = [t.to_dict() for t in Trek.query.filter_by(status='open').all()]
    bookings = [booking_with_trek(b) for b in Booking.query.filter_by(user_id=user_id).all()]
    return jsonify({
        'available_treks': available,
        'bookings': bookings,
    }), 200


@user_bp.route('/treks', methods=['GET'])
@jwt_required()
def treks():
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    q = (request.args.get('q') or '').strip().lower()

    # searching in open treks with q query
    key = f"treks:open:{q}" if q else 'treks:open'
    cached = cache_get(key)
    if cached is not None:
        return jsonify(json.loads(cached)), 200
    query = Trek.query.filter_by(status='open')
    
    # db search
    if q:
        query = query.filter(Trek.name.ilike(f'%{q}%') | Trek.location.ilike(f'%{q}%'))
    data = {'treks': [t.to_dict() for t in query.all()]}
    cache_set(key, json.dumps(data))
    return jsonify(data), 200


@user_bp.route('/bookings', methods=['GET'])
@jwt_required()
def my_bookings():
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    user_id = int(get_jwt_identity())
    bookings = [booking_with_trek(b) for b in Booking.query.filter_by(user_id=user_id).all()]
    return jsonify({'bookings': bookings}), 200


@user_bp.route('/bookings', methods=['POST'])
@jwt_required()
def book_trek():
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    trek_id = data.get('trek_id')

    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404
    if trek.status != 'open':
        return jsonify({'error': 'Trek is not open for booking'}), 400
    if trek.available_slots <= 0:
        return jsonify({'error': 'No slots left'}), 400
    if Booking.query.filter_by(user_id=user_id, trek_id=trek.id, status='booked').first():
        return jsonify({'error': 'You already booked this trek'}), 400
    # if need to limit 1 booking per user here

    booking = Booking(user_id=user_id, trek_id=trek.id, booking_date=datetime.utcnow(), status='booked')
    trek.available_slots -= 1
    
    db.session.add(booking)
    db.session.commit()
    
    # update happened delete the treks cache
    invalidate_treks()
    return jsonify({'message': 'Trek booked', 'booking': booking_with_trek(booking)}), 201


@user_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    user_id = int(get_jwt_identity())
    
    booking = db.session.get(Booking, booking_id)
    if not booking or booking.user_id != user_id:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.status == 'cancelled':
        return jsonify({'error': 'Booking already cancelled'}), 400

    
    booking.status = 'cancelled'
    trek = db.session.get(Trek, booking.trek_id)
    if trek:
        trek.available_slots += 1
    db.session.commit()
    
    invalidate_treks()
    return jsonify({'message': 'Booking cancelled'}), 200


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    address = (data.get('address') or '').strip()
    pin = (data.get('pin') or '').strip()
    phone = (data.get('phone') or '').strip() 

    if phone and user.phone != phone:
        phone_taken = User.query.filter(User.phone == phone, User.id != user.id).first()
        if phone_taken:
            return jsonify({'error': 'Phone number already registered'}), 409

    user.name = name or None
    user.address = address or None
    user.pin = pin or None
    user.phone = phone or None

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200

# ------------------- export ------------------------
@user_bp.route('/export-history', methods=['POST'])
@jwt_required()
def export_history():
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    user_id = int(get_jwt_identity())
    from tasks import export_booking_history_csv

    # creating the task
    result = export_booking_history_csv.delay(user_id) # argument is not time, just passing the id
    return jsonify({'task_id': result.id}), 202
# request creates here ^

@user_bp.route('/export-history/<task_id>', methods=['GET']) # and goes here 
@jwt_required()
def export_history_status(task_id):
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    result = AsyncResult(task_id, app=celery_app)
    if result.state == 'PENDING':
        return jsonify({'status': 'pending'}), 202
    if result.state == 'FAILURE':
        return jsonify({'status': 'failed', 'error': str(result.info)}), 202
    if result.state == 'SUCCESS':
        data = result.get()
        if data.get('error'):
            return jsonify({'status': 'failed', 'error': data['error']}), 202
        return jsonify({**data, 'status': 'ready'}), 200
    return jsonify({'status': 'running'}), 202