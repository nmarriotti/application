from flask_wtf import FlaskForm
from wtforms.fields import StringField, DecimalField, BooleanField, TextAreaField, FileField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
	confirm = PasswordField("Confirm", validators=[DataRequired(), Length(min=7), EqualTo('password', message="Passwords must match!")])