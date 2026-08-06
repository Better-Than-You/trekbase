from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from db.models import db, Staff, Trek, Booking, User

staff_bp = Blueprint('staff', __name__)


# helper to serialize a booking as a trek participant (with the booked user)
def participant(booking):
    user = db.session.get(User, booking.user_id)
    return {
        'id': booking.id,
        'status': booking.status,
        'booking_date': str(booking.booking_date),
        'user': user.to_dict() if user else None,
    }


@staff_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    # only staff can use the dashboard
    if get_jwt().get('role') != 'staff':
        return jsonify({'error': 'Forbidden'}), 403
    staff_id = int(get_jwt_identity())
    staff = db.session.get(Staff, staff_id)
    # only the treks assigned to this staff member, with a participant count
    treks = []
    for t in Trek.query.filter_by(assigned_staff_id=staff_id).all():
        d = t.to_dict()
        d['participants_count'] = Booking.query.filter_by(trek_id=t.id).count()
        treks.append(d)
    return jsonify({'staff': staff.to_dict() if staff else None, 'treks': treks}), 200


@staff_bp.route('/treks/<int:trek_id>', methods=['GET'])
@jwt_required()
def trek_participants(trek_id):
    if get_jwt().get('role') != 'staff':
        return jsonify({'error': 'Forbidden'}), 403
    staff_id = int(get_jwt_identity())
    # a staff member can only view their own assigned treks
    trek = db.session.get(Trek, trek_id)
    if not trek or trek.assigned_staff_id != staff_id:
        return jsonify({'error': 'Trek not found'}), 404

    d = trek.to_dict()
    d['participants'] = [participant(b) for b in Booking.query.filter_by(trek_id=trek.id).all()]
    return jsonify({'trek': d}), 200


@staff_bp.route('/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    if get_jwt().get('role') != 'staff':
        return jsonify({'error': 'Forbidden'}), 403
    staff_id = int(get_jwt_identity())
    trek = db.session.get(Trek, trek_id)
    if not trek or trek.assigned_staff_id != staff_id:
        return jsonify({'error': 'Trek not found'}), 404

    # staff can tweak the available slots and the booking status
    data = request.get_json() or {}
    slots = data.get('available_slots')
    status = (data.get('status') or '').strip()

    if slots is not None:
        try:
            trek.available_slots = max(0, int(slots))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid slots value'}), 400
    if status:
        if status not in ('open', 'closed', 'completed'):
            return jsonify({'error': 'Invalid trek status'}), 400
        trek.status = status

    db.session.commit()
    return jsonify({'message': 'Trek updated', 'trek': trek.to_dict()}), 200