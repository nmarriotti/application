import os
from flask import Flask, url_for
from flask_login import LoginManager

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.debug = True

app.config['SECRET_KEY'] = '\xbc\x15\xc9\xcd\xc1=\x83\xb6\x9c\xf7\xd5\x83\x0b\x0cV\x18\xd1w$\x98\xbck0.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "frontend.login"
login_manager.init_app(app)

from application.backend.routes import back
from application.frontend.routes import mod

import application.models

app.register_blueprint(backend.routes.back, url_prefix='/admin')
app.register_blueprint(frontend.routes.mod)