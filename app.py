from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pymongo
import sys
import logging
from .db import get_db
from datetime import datetime
from  bson.objectid import ObjectId

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.ERROR)

db = get_db()
collection = db['items']

@app.route('/')
def hello_world():
    return 'Hello, World!'
