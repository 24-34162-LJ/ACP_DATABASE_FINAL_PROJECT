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

# ---------------- AUTH ----------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        print("FORM DATA:", form.data)
        print("FORM ERRORS:", form.errors)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):

            session['user_id'] = user.user_id
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['role'] = user.role

            flash('Login successful!', 'success')

            # Redirect based on role
            if session['role'] == 'player':
                return redirect(url_for("commuter"))
            elif session['role'] == 'operator':
                return redirect(url_for("operator"))
            elif session['role'] == 'viewer':
                return redirect(url_for("commuter"))
            else:
                return redirect(url_for("admin"))

        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        role = form.role.data
        email = form.email.data
        password = form.password.data

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already registered. Try another.", "danger")
            return redirect(url_for("sign"))

        hashed_pw = generate_password_hash(password)

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_pw,
            role=role,
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! You may now log in.", "success")
        return redirect(url_for("login"))

    return render_template("sign.html", form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


@app.route("/")
def index():
    return redirect(url_for("home"))

if __name__ == "__main__":
  app.run(debug=True)