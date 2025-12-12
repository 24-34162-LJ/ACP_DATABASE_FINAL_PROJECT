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
    
class Terminal(db.Model):

    __tablename__ = "terminals"

    terminal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    terminal_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)

    status = db.Column(
        db.Enum('active', 'inactive', name='terminal_status'),
        nullable=False,
        default='active'
    )
    
    is_main = db.Column(db.Boolean, default=False, nullable=False)

    # to relationship

    origin_route = db.relationship(
        "Route",
        foreign_keys='Route.start_terminal_id',
        back_populates="start_terminal"
    )

    destination_route = db.relationship(
        "Route",
        foreign_keys='Route.end_terminal_id',
        back_populates="end_terminal"
    )

    origin_trip_pk = db.relationship(
        "Trip",
        foreign_keys='Trip.origin_terminal_id',
        back_populates="origin_fk"
    )

    destination_trip_pk = db.relationship(
        "Trip",
        foreign_keys='Trip.destination_terminal_id',
        back_populates="destination_fk"
    )

    terminal_jeep_pk = db.relationship(
        "TerminalJeepneys",
        foreign_keys='TerminalJeepneys.terminal_id',
        back_populates='terminal_jeep_fk',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    favorite_terminal_pk = db.relationship(
        "Userfavorite",
        foreign_keys='Userfavorite.terminal_id',
        back_populates='favorite_terminal_fk',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<terminal {self.terminal_name}>"
    
class Route(db.Model):

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_name = db.Column(db.String(100), nullable=False)

    start_terminal_id = db.Column(
        db.Integer,
        db.ForeignKey('terminals.terminal_id'),
        nullable=False
    )

    end_terminal_id = db.Column(
        db.Integer,
        db.ForeignKey('terminals.terminal_id'),
        nullable=False
    )

    estimated_time_minutes = db.Column(
        db.Integer,
        nullable=False
    )
    # to relation

    start_terminal = db.relationship(
        "Terminal",
        foreign_keys=[start_terminal_id],
        back_populates="origin_route"
    )

    end_terminal = db.relationship(
        "Terminal",
        foreign_keys=[end_terminal_id],
        back_populates="destination_route"
    )

    trip_pk = db.relationship(
        "Trip",
        foreign_keys='Trip.route_id',
        back_populates="route_fk",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    favorite_route_pk = db.relationship(
        "Userfavorite",
        foreign_keys='Userfavorite.route_id',
        back_populates='favorite_route_fk',
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# jeepneys

class Jeepney(db.Model):
    __tablename__ = "jeepneys"

    jeepney_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate_number = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum('Available', 'En Route', 'Maintenance', 'Inactive', name='jeep_status'),
        nullable=False,
        default='Available'
    )

    trip_pk = db.relationship(
        "Trip",
        foreign_keys="Trip.jeepney_id",
        back_populates="jeepney_fk",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    jeep_jeep_pk = db.relationship(
        "TerminalJeepneys",
        foreign_keys="TerminalJeepneys.jeepney_id",
        back_populates='jeep_jeep_fk',
        cascade="all, delete-orphan",
        passive_deletes=True
    )