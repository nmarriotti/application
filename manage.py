#! /usr/bin/python
from application import app
from application.models import db, User
from flask_script import Manager, prompt_bool
import os, sys, uuid
from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == "__main__":
	try:
		if sys.argv[1] == 'initdb':
			db.create_all()
			admin_user = User(public_id=uuid.uuid4().hex, username="admin", password_hash=generate_password_hash("admin"), admin=True)
			db.session.add(admin_user)
			db.session.commit()
			print('Initialized the database; admin user created.')
		elif sys.argv[1] == 'dropdb':
			db.drop_all()
			print('Dropped the database')
	except:
		port = int(os.environ.get('PORT', 5000))
		app.run(host='0.0.0.0', port=port)