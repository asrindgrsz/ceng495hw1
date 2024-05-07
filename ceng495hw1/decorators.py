from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:  # Check if user is logged in
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function
