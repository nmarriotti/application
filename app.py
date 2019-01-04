from flask import Flask, flash, render_template, request, redirect, url_for, g, session, abort
from sqlalchemy.orm import sessionmaker
from tabledef_users import *
import os
engine = create_engine('sqlite:///data.db', echo=True)

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return "Hello World"

@app.route('/login', methods=['POST'])
def do_login():

	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])

	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	
	if result:
		session['logged_in'] = True
	else:
		flash('Access denied')
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
