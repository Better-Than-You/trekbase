import os
from db.models import db, User


def seed_admin():
    email = os.getenv('ADMIN_EMAIL', 'admin@trekbase.com')
    password = os.getenv('ADMIN_PASSWORD', 'admin123')
    if not User.query.filter_by(email=email).first():
        admin = User(email=email, name='Admin', role='admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
