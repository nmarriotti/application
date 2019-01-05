from flask import Blueprint, render_template, url_for, request, json, jsonify, redirect, flash, abort
from flask_login import current_user, login_user, logout_user
from application.models import db, User
from application import login_manager, app
import uuid
import datetime
import jwt
from .forms import LoginForm, ChangePasswordForm
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

@back.route('/delete/<userid>')
@admin_required
def delete_user(userid):
	user = User.query.filter_by(public_id=userid).first()
	if user:
		db.session.delete(user)
		db.session.commit()
		flash(user.username + " has been deleted")
		return redirect(url_for('backend.users'))

@back.route('/changepassword/<userid>', methods=['GET', 'POST'])
@admin_required
def change_pass(userid):
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(public_id=userid).first()
		if user:
			# create user
			user.password_hash=generate_password_hash(form.password.data)
			db.session.commit()
			flash(user.username + "'s password has been updated")
			return redirect(url_for('backend.users'))
		else:
			flash('User not found')
	else:
		user = User.query.filter_by(public_id=userid).first()
		if user:
			return render_template('backend/changepassword.html', username=user.username, form=form)
		else:
			flash("User not found")
	return redirect(url_for('backend.users'))

@back.route('/makeadmin/<userid>')
@admin_required
def make_admin(userid):
	user = User.query.filter_by(public_id=userid).first()
	if user:
		user.admin = True
		db.session.commit()
		flash(user.username + " is now an administrator")
	return redirect(url_for('backend.users'))

@back.route('/makestandard/<userid>')
@admin_required
def make_standard(userid):
	user = User.query.filter_by(public_id=userid).first()
	if user:
		user.admin = False
		db.session.commit()
		flash(user.username + " is now a standard user")
	return redirect(url_for('backend.users'))

