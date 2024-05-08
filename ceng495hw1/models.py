from werkzeug.security import generate_password_hash
from .db import get_db
from bson.objectid import ObjectId
from werkzeug.exceptions import BadRequest
from datetime import datetime


def create_user(email, password, name, phone):
    """Create a new user in the database with hashed password."""
    db = get_db()
    hashed_password = generate_password_hash(password)
    db.users.insert_one({
        "email": email,
        "password": hashed_password,
        "name": name,
        "phone": phone,
        "admin": False
    })

def get_user_by_email(email):
    """Retrieve a user from the database by email."""
    db = get_db()
    return db.users.find_one({"email": email})

def add_item(item_data):
    """
    Add a new item to the MongoDB collection.
    Ensure required fields are present before insertion.
    """
    db = get_db()
    # Validate required fields
    required_fields = ["title", "category", "price", "image", "description"]
    for field in required_fields:
        if field not in item_data:
            raise BadRequest(f"Missing required field: {field}")

    # Validate category
    valid_categories = ["vehicles", "computers", "phones", "private_lessons"]
    if item_data["category"] not in valid_categories:
        raise BadRequest(f"Invalid category: {item_data['category']}")

    # Ensure the title and category are unique
    existing_item = db.items.find_one({
        "title": item_data["title"],
        "category": item_data["category"]
    })
    if existing_item:
        raise BadRequest("An item with this title and category already exists.")

    # Add a timestamp for when the item was created
    item_data["created_at"] = datetime.now()

    # Insert the item into MongoDB
    result = db.items.insert_one(item_data)

    return result.inserted_id  # Return the ObjectId of the newly created item
