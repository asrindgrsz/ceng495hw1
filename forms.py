from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError

def validate_ceng_metu_email(form, field):
    """Custom validator to ensure email is from ceng.metu.edu.tr domain."""
    if not field.data.endswith("@ceng.metu.edu.tr"):
        raise ValidationError("Registration is restricted to ceng.metu.edu.tr domain.")

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
    name = StringField("Name", validators=[InputRequired(), Length(min=2, max=50)])
    phone = StringField("Phone", validators=[InputRequired(), Regexp(r'^\+?[0-9]{10,15}$', message="Invalid phone number")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
    submit = SubmitField("Login")
