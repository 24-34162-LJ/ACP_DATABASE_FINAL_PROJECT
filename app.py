from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, AddTerminal
from models import db, User, Terminal

# ---------------- FLASK APP SETUP ----------------
app = Flask(__name__)

app.config['SECRET_KEY'] = 'lj123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jeep.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

db.init_app(app)

if __name__ == "__main__":
  app.run(debug=True)