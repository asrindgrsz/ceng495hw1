from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from .models import add_item
from .forms import CreateItemForm, UpdateListingForm
from .decorators import login_required
from .db import get_db
from bson.objectid import ObjectId
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, IntegerField, FormField, FieldList
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError, NumberRange, Optional


bp = Blueprint("item", __name__, url_prefix="/")

@bp.route('/item', methods=["GET", "POST"])
#@login_required
def create_item():
    form = CreateItemForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Gather common attributes
            item_data = {
                "category": form.category.data,
                "title": form.title.data,
                "description": form.description.data,
                "image": form.image.data,
                "price": form.price.data,
            }

            # Handle category-specific attributes manually
            category = form.category.data
            if category == "vehicles":
                item_data["type"] = request.form.get("type")
                item_data["brand"] = request.form.get("brand")
                item_data["model"] = request.form.get("model")
                item_data["year"] = int(request.form.get("year"))
                item_data["color"] = request.form.get("color")
                item_data["engine_displacement"] = int(request.form.get("engine_displacement"))
                item_data["fuel_type"] = request.form.get("fuel_type")
                item_data["transmission_type"] = request.form.get("transmission_type")
                item_data["mileage"] = int(request.form.get("mileage"))
            elif category == "computers":
                item_data["processor"] = request.form.get("processor_pc")
                item_data["ram_pc"] = int(request.form.get("ram_pc"))
                item_data["storage_pc"] = int(request.form.get("storage_pc"))
                item_data["graphics_card"] = request.form.get("graphics_card")
                item_data["operating_system"] = request.form.get("operating_system_pc")
            elif category == "phones":
                item_data["brand"] = request.form.get("brand_phone")
                item_data["model"] = request.form.get("model_phone")
                item_data["production_date"] = int(request.form.get("production_date"),base=10)
                item_data["operating_system"] = request.form.get("operating_system_phone")
                item_data["processor"] = request.form.get("processor_phone")
                item_data["ram_phone"] = int(request.form.get("ram_phone"), base=10)
                item_data["storage_phone"] = int(request.form.get("storage_phone"),base=10)
                item_data["camera_specs"] = request.form.get("camera_specs")
                item_data["battery_capacity"] = int(request.form.get("battery_capacity"),base=10)
            elif category == "private_lessons":
                item_data["tutor_name"] = request.form.get("tutor_name")
                item_data["lessons"] = request.form.get("lessons")
                item_data["location"] = request.form.get("location")
                item_data["duration"] = int(request.form.get("duration"),base=10)

            # Add custom attributes
            custom_keys = request.form.getlist("custom_attribute_key[]")
            custom_values = request.form.getlist("custom_attribute_value[]")
            for key, value in zip(custom_keys, custom_values):
                item_data[key] = value

            item_data["owner"] = session.get('email')
            # Add the item to the database
            add_item(item_data)
            flash("Item created successfully!", "success")
            return redirect(url_for("item.index"))

    return render_template("create_item.html", form=form)

@bp.route("/")
def index():
    # Retrieve the last 100 added listings, sorted by creation date (most recent first)
    db = get_db()
    last_100_listings = db.items.find().sort("created_at", -1).limit(100)

    return render_template("index.html", listings=last_100_listings)

@bp.route('/listing/<listing_id>')
def view_listing(listing_id):
    db = get_db()
    listing = db.items.find_one({"_id": ObjectId(listing_id)})
    user = db.users.find_one({"email": listing["owner"]})
    if not listing:
        flash("Listing not found.", "warning")
        return redirect(url_for("item.index"))  # Redirect back to listings if not found
    
    return render_template("listing.html", listing=listing, user=user)


@bp.route('/category/<category>')
def category_listings(category):
    # Retrieve all listings for the specified category, sorted by date (most recent first)
    db = get_db()
    category_listings = db.items.find({"category": category}).sort("created_at", -1)

    return render_template("category_listings.html", category=category, listings=category_listings)


@bp.route('/delete_listing/<listing_id>')
def delete_listing(listing_id):
    db = get_db()
    listing = db.items.find_one({"_id": ObjectId(listing_id)})

    if not listing:
        flash("Listing not found.", "warning")
        return redirect(url_for("item.index"))

    # Ensure the user is the owner
    if session.get("email") != listing.get("owner"):
        flash("You are not authorized to delete this listing.", "danger")
        return redirect(url_for("item.index"))

    # Delete the listing from the database
    db.items.delete_one({"_id": ObjectId(listing_id)})

    flash("Listing deleted successfully!", "success")
    return redirect(url_for("item.index"))


@bp.route('/update_listing/<listing_id>', methods=["GET", "POST"])
def update_listing(listing_id):
    db = get_db()
    listing = db.items.find_one({"_id": ObjectId(listing_id)})

    if not listing:
        flash("Listing not found.", "warning")
        return redirect(url_for("item.index"))

    # Ensure the user is the owner
    if session.get("email") != listing.get("owner"):
        flash("You are not authorized to update this listing.", "danger")
        return redirect(url_for("item.index"))
    
    form = UpdateListingForm()

    if request.method == "POST" and form.validate_on_submit():
        # Update listing with new data
        update_data = listing
        for key in request.form:
            update_data[key] = request.form[key]

        # Update the listing in the database
        db.items.update_one({"_id": ObjectId(listing_id)}, {"$set": update_data})

        flash("Listing updated successfully!", "success")
        return redirect(url_for("item.index"))  # Redirect to the listings page

    return render_template("update_listing.html", form=form, listing=listing)
