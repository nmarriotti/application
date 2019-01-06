from flask import Blueprint, render_template, url_for, request, json, jsonify, redirect, flash, abort
from application.models import db, User, Part, Tracker
from application import login_manager, app
from flask_login import current_user, login_required, login_user, logout_user
from .forms import LoginForm, RegisterForm, SearchForm, CheckoutPart
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

@mod.route('/view/<partid>', methods=['GET','POST'])
@login_required
def view_part(partid):
	form = CheckoutPart()
	part = Part.query.filter_by(partnum=partid).first()
	if form.validate_on_submit():
		if form.quantity.data > part.available_qty:
			flash("Quantity exceeds available!")
		else:
			# check if user already has the same part
			samepart = Tracker.query.filter_by(username=current_user.username,partid=part.id).first()
			if samepart:
				samepart.quantity += form.quantity.data
				part.available_qty -= form.quantity.data
				db.session.commit()
			else:
				mypart = Tracker(username=current_user.username,partid=part.id,quantity=form.quantity.data,date_out=datetime.datetime.now(), partnum=part.partnum,partname=part.name)
				part.available_qty -= form.quantity.data
				db.session.add(mypart)
				db.session.commit()
			return redirect(url_for('frontend.index'))
	if part:
		return render_template('frontend/view.html', part=part, form=form)

@mod.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('frontend.index'))

@mod.route('/browse', methods=['GET','POST'])
@login_required
def browse():
	showResults=0
	results=''
	form = SearchForm()
	#parts = Part.query.all()
	if form.validate_on_submit():
		if form.choices.data == 'partnum':
			results = Part.query.filter(Part.partnum.like("%"+form.search.data+"%")).all()
		if form.choices.data == 'partname':
			results = Part.query.filter(Part.name.like("%"+form.search.data+"%")).all()
		if form.choices.data == 'Vendor':
			results = Part.query.filter(Part.vendor.like("%"+form.search.data+"%")).all()
		showResults=1
	if len(results) > 0:
		return render_template('frontend/browse.html', hasParts=1, form=form, results=results,showResults=showResults)
	return render_template('frontend/browse.html', hasParts=0, form=form, results=results,showResults=showResults)

@mod.route('/dashboard')
@login_required
def dashboard():
	myparts = Tracker.query.filter_by(username=current_user.username).all()
	if myparts:
		return render_template('frontend/index.html', myparts=myparts, hasparts=1)
	myparts=0
	return render_template('frontend/index.html', myparts=0, hasparts=0)


@mod.route('/')
@login_required
def index():
	return redirect(url_for('frontend.browse'))
		
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

