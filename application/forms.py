from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email

class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])

class RegisterForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email() ])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
	confirm = PasswordField("Confirm", validators=[DataRequired(), Length(min=7), EqualTo('password', message="Passwords must match!")])