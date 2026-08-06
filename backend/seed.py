#!/usr/bin/env python3
"""Seed the database with a few dummy users, staff, treks and bookings.

Run from the backend directory (same place the Flask app runs so the SQLite
file is created in backend/instance/):

    cd backend
    .venv/bin/python seed.py
"""

import random
from datetime import date, timedelta, datetime

from app import app
from db.models import db, User, Staff, Trek, Booking

# (name, email, password, phone, address, pin)
USERS = [
    ("user1", "user1@email.com", "user1", "9800000101", "Thamel, Kathmandu", "44600"),
    ("user2", "user2@email.com", "user2", "9800000102", "Lakeside, Pokhara", "33700"),
    ("user3", "user3@email.com", "user3", "9800000103", "Boudha, Kathmandu", "44600"),
]

# (name, contact, email, password, status)
STAFF = [
    ("staff1", "9800000001", "staff1@email.com", "staff1", "available"),
    ("staff2", "9800000002", "staff2@email.com", "staff2", "available"),
    ("staff3", "9800000003", "staff3@email.com", "staff3", "not_available"),
]

# (name, location, difficulty, duration_days, available_slots)
TREKS = [
    ("Everest Base Camp", "Solukhumbu", "hard", 14, 12),
    ("Annapurna Circuit", "Manang", "hard", 12, 10),
    ("Langtang Valley", "Rasuwa", "moderate", 7, 20),
    ("Mardi Himal", "Kaski", "moderate", 5, 18),
    ("Mera Peak", "Sankhuwasabha", "hard", 16, 8),
    ("Upper Mustang", "Mustang", "moderate", 11, 15),
    ("Ghorepani Poon Hill", "Myagdi", "easy", 4, 25),
    ("Helambu Trek", "Sindhupalchok", "easy", 6, 16),
]

STATUSES = ["pending", "approved", "open", "open", "open", "completed"]


def main():
    with app.app_context():
        users = _add_users()
        staff = _add_staff()
        treks = _add_treks(staff)
        bookings = _add_bookings(users, treks)

        db.session.commit()

        print("\nSeeding complete.")
        print(f"  users   : {len(users)} added")
        print(f"  staff   : {len(staff)} added")
        print(f"  treks   : {len(treks)} added")
        print(f"  bookings: {len(bookings)} added")
        print("Existing admin (admin@trekbase.com / admin123) is kept untouched.")


def _add_users():
    added = []
    for name, email, password, phone, address, pin in USERS:
        if User.query.filter_by(email=email).first():
            print(f"  user {email} already exists, skipping")
            continue
        u = User(email=email, name=name, phone=phone, address=address, pin=pin)
        u.set_password(password)
        db.session.add(u)
        added.append(u)
    db.session.flush()
    return added


def _add_staff():
    added = []
    for name, contact, email, password, status in STAFF:
        if Staff.query.filter_by(email=email).first():
            print(f"  staff {email} already exists, skipping")
            continue
        s = Staff(name=name, contact=contact, email=email, status=status)
        s.set_password(password)
        db.session.add(s)
        added.append(s)
    db.session.flush()
    return added


def _pick_dates(status, duration_days):
    today = date.today()
    offset = random.randint(10, 60)
    if status == "completed":
        start = today - timedelta(days=offset)
    else:
        start = today + timedelta(days=offset)
    end = start + timedelta(days=duration_days)
    return start, end


def _add_treks(staff):
    added = []
    pool = [s for s in staff if s.status == "available"] or staff

    for name, location, difficulty, duration, slots in TREKS:
        status = random.choice(STATUSES)
        start, end = _pick_dates(status, duration)
        t = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration_days=duration,
            available_slots=slots,
            assigned_staff_id=random.choice(pool).id if pool else None,
            status=status,
            start_date=start,
            end_date=end,
        )
        db.session.add(t)
        added.append(t)
    db.session.flush()
    return added


def _add_bookings(users, treks):
    if not users or not treks:
        return []
    added = []
    random.shuffle(users)
    for i, u in enumerate(users):
        for t in treks[i::len(users)]:
            if random.random() < 0.7:
                status = "completed" if t.status == "completed" else "booked"
                book_date = t.start_date - timedelta(days=random.randint(1, 5))
                b = Booking(
                    user_id=u.id,
                    trek_id=t.id,
                    booking_date=datetime.combine(book_date, datetime.min.time()),
                    status=status,
                )
                db.session.add(b)
                added.append(b)
    db.session.flush()
    return added


if __name__ == "__main__":
    main()
