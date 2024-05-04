from werkzeug.security import generate_password_hash
from .db import get_db
from app import mongo

def create_user(email, password, name, phone):
    """Create a new user in the database with hashed password."""
    db = get_db()
    hashed_password = generate_password_hash(password)
    db.users.insert_one({
        "email": email,
        "password": hashed_password,
        "name": name,
        "phone": phone,
    })

def get_user_by_email(email):
    """Retrieve a user from the database by email."""
    return db.users.find_one({"email": email})
