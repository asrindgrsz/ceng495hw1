from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, IntegerField, FormField, FieldList
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError, NumberRange, Optional

class CreateItemForm(FlaskForm):
    category = SelectField("Category", choices=[
        ("vehicles", "Vehicles"),
        ("computers", "Computers"),
        ("phones", "Phones"),
        ("private_lessons", "Private Lessons")
    ], validators=[InputRequired()])

    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=100)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(min=10)])
    image = StringField("Image URL", validators=[InputRequired(), Length(min=1)])
    price = FloatField("Price", validators=[InputRequired()])

def validate_ceng_metu_email(form):
    """Custom validator to ensure email is from ceng.metu.edu.tr domain."""
    if not str(form.data['email']).split('@')[-1]=='ceng.metu.edu.tr':
        raise ValidationError("Registration is restricted to ceng.metu.edu.tr domain.")
    return True

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
    

class UpdateListingForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(min=1, max=100)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(min=10)])
    image = StringField("Image URL", validators=[Optional(), Length(min=1)])
    price = FloatField("Price", validators=[InputRequired()])

    # Static category (cannot be changed)
    category = StringField("Category", render_kw={"readonly": True})
        
    def __init__(self, listing=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if listing:
            self.title.data = listing.get("title", "")
            self.description.data = listing.get("description", "")
            self.image.data = listing.get("image", "")
            self.price.data = listing.get("price", 0.0)
            self.category.data = listing.get("category", "")