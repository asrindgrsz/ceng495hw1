from flask import Flask
from pymongo import MongoClient
import os
import logging
from datetime import datetime
from  bson.objectid import ObjectId

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.ERROR)

MONGO_URI = "mongodb+srv://e2380301:ceng495hw1@cluster0.9pjmxxw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@app.route('/')
def hello_world():
    return 'Hello, World!'
