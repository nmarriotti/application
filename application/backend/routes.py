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
	return render_template('backend/users.html')

@back.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user:
        	if user.check_password(form.password.data):
	            login_user(user)
	            print(current_user.is_authenticated)
	            return redirect(request.args.get('next') or url_for('backend.index'))
        flash('Invalid username and/or password.')
    return render_template('backend/auth/login.html', form=form)

@back.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('backend.login'))





