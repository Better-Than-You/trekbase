from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from db.models import db, User, Staff, Trek, Booking

admin_bp = Blueprint('admin', __name__)

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
    bookings = [booking_with_details(b) for b in Booking.query.all()]
    staff = [s.to_dict() for s in Staff.query.all()]
    users = [u.to_dict() for u in User.query.all()]

    return jsonify({
        'counts': {
            'bookings': len(bookings),
            'staff': len(staff),
            'users': len(users),
        },
        'bookings': bookings,
        'staff': staff,
        'users': users,
    }), 200