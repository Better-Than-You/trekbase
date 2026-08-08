import os
from dotenv import load_dotenv
from db.models import db, User

load_dotenv()

# seeding admin
def seed_admin():
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@trekbase.com')
    password = os.getenv('ADMIN_PASSWORD', 'admin123') # very strong password as fallback
    if not User.query.filter_by(email=ADMIN_EMAIL).first():
        admin = User(email=ADMIN_EMAIL, name='Admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
