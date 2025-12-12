from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import text
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model,  UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.Enum('player', 'operator', 'viewer', 'admin', name='user_roles'),
        nullable=False,
        default='player'
    )

    level = db.Column(db.Integer, nullable=False, default=1)
    xp_points = db.Column(db.Integer, nullable=False, default=0)

    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # relations (with cascade)

    favorite_pk = db.relationship(
        "Userfavorite",
        foreign_keys='Userfavorite.user_id',
        back_populates='favorite_fk',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    notification_pk = db.relationship(
        "Notification",
        foreign_keys='Notification.user_id',
        back_populates='notification_fk',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    audit_user_pk = db.relationship(
        "Auditlog",
        foreign_keys='Auditlog.user_id',
        back_populates='audit_user_fk',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"