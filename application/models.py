from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from application import app
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(120), unique=True)
	password_hash = db.Column(db.String)
	admin = db.Column(db.Boolean, default=False)
	created_on = db.Column(db.DateTime, default=datetime.datetime.now())
	
	@property
	def password(self):
		raise AttributeError('password: write-only field')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	@staticmethod
	def get_by_username(username):
		return User.query.filter_by(username=username).first()

	def __repr__(self):
		return "<User '{}'>".format(self.username)

class Part(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	partnum = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))
	vendor = db.Column(db.String(30))
	location = db.Column(db.String(30))
	desired_qty = db.Column(db.Integer)
	quantity = db.Column(db.Integer, default=0)
	available_qty = db.Column(db.Integer, default=0)

class Tracker(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	partid = db.Column(db.Integer)
	partnum = db.Column(db.String(50))
	partname = db.Column(db.String(50))
	quantity = db.Column(db.Integer)
	date_in = db.Column(db.Integer)
	date_out = db.Column(db.DateTime)



