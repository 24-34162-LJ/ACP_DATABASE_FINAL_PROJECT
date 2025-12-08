from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import text

db = SQLAlchemy()

class User(db.Model):
    _tablename_ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('player', 'operator', 'viewer', 'admin', name='user_roles'), nullable=False, default='player')
    level = db.Column(db.Integer, nullable=False, default=1)
    xp_points = db.Column(db.Integer, nullable=False, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # relationships...