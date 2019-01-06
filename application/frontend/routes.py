from flask import Blueprint, render_template, url_for, request, json, jsonify, redirect, flash, abort
from application.models import db, User, Part, Tracker
from application import login_manager, app
from flask_login import current_user, login_required, login_user, logout_user
from .forms import LoginForm, RegisterForm, SearchForm
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import datetime
import jwt
from functools import wraps

mod = Blueprint('frontend', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

def login_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if current_user.is_authenticated:
			is_logged_in = True
		else:
			return redirect(url_for('frontend.login'))
		return f(*args, **kwargs)
	return decorated

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		if not token:
			return jsonify({'message' : 'Token is missing!'}), 401
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			abort(400)
		return f(*args, **kwargs)
	return decorated

@mod.route('/view/<partid>')
@login_required
def view_part(partid):
	part = Part.query.filter_by(partnum=partid).first()
	if part:
		return render_template('frontend/view.html', part=part)

@mod.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('frontend.index'))

@mod.route('/browse')
@login_required
def browse():
	formsearch = SearchForm()
	parts = Part.query.all()
	return render_template('frontend/browse.html', formsearch=formsearch, parts=parts)

@mod.route('/')
@login_required
def index():
	myparts = Tracker.query.filter_by(username=current_user.username).first()
	if not myparts:
		myparts=0
	return render_template('frontend/index.html', myparts=myparts)

@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user:
        	if user.check_password(form.password.data):
	            login_user(user)
	            return redirect(request.args.get('next') or url_for('frontend.index'))
        flash('Invalid username and/or password.')
    return render_template('frontend/auth/login.html', form=form)


@mod.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not user:
			# create user
			new_user = User(public_id=uuid.uuid4().hex, username=form.username.data, password_hash=generate_password_hash(form.password.data))
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user)
			return redirect(url_for('frontend.index'))
		flash('Username already taken!')
	return render_template('frontend/auth/register.html', form=form)

@mod.route('/account')
@login_required
def myaccount():
	return "This is the account page for: {}".format(current_user.email)

