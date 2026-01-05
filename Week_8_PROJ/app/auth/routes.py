from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    return "Login Page (implement form)"

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
