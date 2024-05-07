import os
import pymongo
import logging
from functools import wraps
from flask import session, redirect, url_for, flash, Flask



def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'abc'

    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    

    # register the database commands
    #from . import db

    #db.init_app(app)

    # apply the blueprints to the app
    from . import auth
    from . import item
    logging.basicConfig(filename='app.log', level=logging.ERROR)
    #from . import blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(item.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    #app.add_url_rule("/", endpoint="index")

    return app