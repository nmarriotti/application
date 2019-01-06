from flask_wtf import FlaskForm
from wtforms.fields import StringField, DecimalField, IntegerField, FileField, BooleanField, TextAreaField, FileField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
	confirm = PasswordField("Confirm", validators=[DataRequired(), Length(min=7), EqualTo('password', message="Passwords must match!")])

class PartForm(FlaskForm):
	partnum = StringField("Part #", validators=[DataRequired()])
	name = StringField("Description", validators=[DataRequired()])
	vendor = StringField("Vendor", validators=[DataRequired()])
	location = StringField("Location", validators=[DataRequired()])
	desired_qty = IntegerField("Desired Quantity", validators=[DataRequired()])
	quantity = IntegerField("Quantity")

class UploadForm(FlaskForm):
    file = FileField()