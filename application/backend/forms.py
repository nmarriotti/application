from flask_wtf import FlaskForm
from wtforms.fields import StringField, DecimalField, BooleanField, TextAreaField, FileField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])