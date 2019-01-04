from flask import Blueprint, render_template, url_for, request, json, jsonify, redirect, flash, abort
from flask_login import current_user, login_user, logout_user
from application.models import db, User
from application import login_manager, app
import uuid
import datetime
import jwt
from .forms import LoginForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

back = Blueprint('backend', __name__, template_folder='templates')

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

def admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if current_user.is_authenticated and current_user.admin:
			is_admin = True
		else:
			return redirect(url_for('backend.login'))
		return f(*args, **kwargs)
	return decorated

@back.route('/')
@admin_required
def index():
	return render_template('backend/index.html')

@back.route('/users')
@admin_required
def users():
	users = User.query.all()
	return render_template('backend/users.html', users=users)

@back.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('frontend.login'))

@back.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('backend.login'))





