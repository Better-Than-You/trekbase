import os
from flask import Flask
from flask_jwt_extended import JWTManager
from db.models import db
from db import seed_admin
from routes import auth_bp, admin_bp, user_bp, staff_bp

# ---------------- config ----------------
# settings come from .env with safe fallbacks
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-jwt-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400

# ---------------- db & jwt init ----------------
db.init_app(app)
JWTManager(app)

# create tables on boot and make sure the admin account exists
with app.app_context():
    db.create_all()
    seed_admin()

# ---------------- routes ----------------
# each blueprint is mounted under its own /api/... prefix
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(staff_bp, url_prefix='/api/staff')

if __name__ == '__main__':
    app.run(debug=True)
