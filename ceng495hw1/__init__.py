import os
import pymongo
import logging
from functools import wraps
from flask import session, redirect, url_for, flash, Flask



def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'abc'
    

    # register the database commands
    #from . import db

    #db.init_app(app)

    # apply the blueprints to the app
    from . import auth
    from . import item
    logging.basicConfig(filename='app.log', level=logging.ERROR)

    app.register_blueprint(auth.bp)
    app.register_blueprint(item.bp)

    return app