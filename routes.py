from flask import render_template, redirect, url_for, flash, session
from app import app
from .forms import RegistrationForm, LoginForm
from .models import create_user, get_user_by_email
from werkzeug.security import check_password_hash

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email domain is valid
        if not form.email.data.endswith("@ceng.metu.edu.tr"):
            flash("Registration is restricted to ceng.metu.edu.tr email addresses.", "danger")
            return render_template("register.html", form=form)

        # Check if the email already exists in the database
        existing_user = get_user_by_email(form.email.data)
        if existing_user:
            flash("This email is already registered. Please log in.", "danger")
            return redirect(url_for("login"))

        # Create a new user
        create_user(form.email.data, form.password.data, form.name.data, form.phone.data)
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user and check_password_hash(user['password'], form.password.data):
            session["email"] = user["email"]
            session["name"] = user["name"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))  # Redirect to a secured page
        
        flash("Invalid credentials. Please try again.", "danger")
    
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    session.pop("email", None)
    session.pop("name", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))
