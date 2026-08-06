from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from db.models import db, User, Trek, Booking
from datetime import datetime

user_bp = Blueprint('user', __name__)


# helper to serialize a booking with its trek
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
    # only trekkers can use the dashboard
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    user_id = int(get_jwt_identity())
    # open treks they can book, plus the treks they already booked
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
    query = Trek.query.filter_by(status='open')
    # optional search filters open treks by name or location
    if q:
        query = query.filter(Trek.name.ilike(f'%{q}%') | Trek.location.ilike(f'%{q}%'))
    return jsonify({'treks': [t.to_dict() for t in query.all()]}), 200


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

    # sanity checks before letting the booking go through
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({'error': 'Trek not found'}), 404
    if trek.status != 'open':
        return jsonify({'error': 'Trek is not open for booking'}), 400
    if trek.available_slots <= 0:
        return jsonify({'error': 'No slots left'}), 400
    if Booking.query.filter_by(user_id=user_id, trek_id=trek.id, status='booked').first():
        return jsonify({'error': 'You already booked this trek'}), 400

    # create the booking and free up one slot
    booking = Booking(user_id=user_id, trek_id=trek.id, booking_date=datetime.utcnow(), status='booked')
    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Trek booked', 'booking': booking_with_trek(booking)}), 201


@user_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    if get_jwt().get('role') != 'user':
        return jsonify({'error': 'Forbidden'}), 403
    user_id = int(get_jwt_identity())
    # a user can only cancel their own, still-active booking
    booking = db.session.get(Booking, booking_id)
    if not booking or booking.user_id != user_id:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.status == 'cancelled':
        return jsonify({'error': 'Booking already cancelled'}), 400

    # mark as cancelled and give the slot back to the trek
    booking.status = 'cancelled'
    trek = db.session.get(Trek, booking.trek_id)
    if trek:
        trek.available_slots += 1
    db.session.commit()
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

    # email is not changeable
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    address = (data.get('address') or '').strip()
    pin = (data.get('pin') or '').strip()
    phone = (data.get('phone') or '').strip() 

    # phone is optional but unique
    if phone and user.phone != phone:
        phone_taken = User.query.filter(User.phone == phone, User.id != user.id).first()
        if phone_taken:
            return jsonify({'error': 'Phone number already registered'}), 409

    if name:
        user.name = name
    user.address = address or None
    user.pin = pin or None
    user.phone = phone or None

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200