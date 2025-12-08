from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify, current_app, abort
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, AddTerminal
from models import (
    db, User, Terminal, Jeepney, Trip, Seat, TerminalJeepneys,
    Route, Auditlog, Userfavorite, Notification
)

from forms import (
    UserForm, TerminalForm, RouteForm, JeepneyForm,
    TripForm, SeatForm, TerminalJeepneysForm,
    UserfavoriteForm, NotificationForm, AuditlogForm
)

from datetime import datetime
from sqlalchemy import func

# ---------------- GLOBAL CONSTANTS ----------------
MAIN_TERMINAL_ID = 1

# ---------------- FLASK APP SETUP ----------------
app = Flask(__name__)

app.config['SECRET_KEY'] = 'lj123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jeep.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

db.init_app(app)

# ---------------- BASIC PAGES ----------------
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    data = {
       "users": User.query.all(),
       "terminals": Terminal.query.all(),
       "jeepneys": Jeepney.query.all(),
       "terminal_queue": TerminalJeepneys.query.all(),
       "trips": Trip.query.all(),
       "seats": Seat.query.all(),
       "routes": Route.query.all(),
       "favorites": Userfavorite.query.all(),
       "notifications": Notification.query.all(),
       "auditlogs": Auditlog.query.all(),
   }
    return render_template("view_database.html", data=data) 

if __name__ == "__main__":
  app.run(debug=True)