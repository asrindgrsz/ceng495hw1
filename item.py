from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from .models import add_item
from .forms import CreateItemForm
from .decorators import login_required
from .db import get_db

bp = Blueprint("item", __name__, url_prefix="/item")

@bp.route('/create_item', methods=["GET", "POST"])
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
                item_data["processor"] = request.form.get("processor")
                item_data["ram"] = int(request.form.get("ram"))
                item_data["storage"] = int(request.form.get("storage"))
                item_data["graphics_card"] = request.form.get("graphics_card")
                item_data["operating_system"] = request.form.get("operating_system")
            elif category == "phones":
                item_data["brand"] = request.form.get("brand")
                item_data["model"] = request.form.get("model")
                item_data["year"] = int(request.form.get("year"))
                item_data["operating_system"] = request.form.get("operating_system")
                item_data["processor"] = request.form.get("processor")
                item_data["ram"] = int(request.form.get("ram"))
                item_data["storage"] = int(request.form.get("storage"))
                item_data["camera_specs"] = request.form.get("camera_specs")
                item_data["battery_capacity"] = int(request.form.get("battery_capacity"))
            elif category == "private_lessons":
                item_data["tutor_name"] = request.form.get("tutor_name")
                item_data["lessons"] = request.form.get("lessons")
                item_data["location"] = request.form.get("location")
                item_data["duration"] = int(request.form.get("duration"))

            # Add custom attributes
            custom_keys = request.form.getlist("custom_attribute_key[]")
            custom_values = request.form.getlist("custom_attribute_value[]")
            for key, value in zip(custom_keys, custom_values):
                item_data[key] = value

            item_data["owner"] = session["email"]
            # Add the item to the database
            add_item(item_data)
            flash("Item created successfully!", "success")
            return redirect(url_for("home"))

    return render_template("create_item.html", form=form)

@bp.route("/")
def index():
    """Show all the posts, most recent first."""

    return render_template("index.html")