import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ======================== USER ============================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    # optional fields
    address = db.Column(db.String)
    pin = db.Column(db.String)
    phone = db.Column(db.String, unique=True) # this is unique for obv reasons
    
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'address': self.address,
            'pin': self.pin,
            'phone': self.phone,
            'is_blacklisted': bool(self.is_blacklisted),
        }

# ======================== STAFF ============================
class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    status = db.Column(db.String, default='available')  # available/assigned/not_available
    
    is_blacklisted = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'email': self.email,
            'status': self.status,
            'is_blacklisted': bool(self.is_blacklisted),
        }

# ======================== TREKS ============================
class Trek(db.Model):
    __tablename__ = 'treks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String, nullable=False)  # easy/moderate/hard
    duration_days = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    status = db.Column(db.String, default='pending')  # Open / Closed / Completed (if admin is the one who is creating the treks, the approved and pending is not needed)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'difficulty': self.difficulty,
            'duration_days': self.duration_days,
            'available_slots': self.available_slots,
            'assigned_staff_id': self.assigned_staff_id,
            'status': self.status,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
        }

# ======================== BOOKINGS ============================
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime)
    status = db.Column(db.String, default='booked')  # booked/cancelled/completed

    def to_dict(self):
        # safe shape to send to the frontend
        return {
            'id': self.id,
            'user_id': self.user_id,
            'trek_id': self.trek_id,
            'booking_date': str(self.booking_date),
            'status': self.status,
        }
