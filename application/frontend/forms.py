from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
	confirm = PasswordField("Confirm", validators=[DataRequired(), Length(min=7), EqualTo('password', message="Passwords must match!")])