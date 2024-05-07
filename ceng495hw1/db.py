import pymongo
import sys

def get_db():
        
    MONGO_URI = "mongodb+srv://e2380301:ceng495hw1@cluster0.9pjmxxw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    try:
        client = pymongo.MongoClient(MONGO_URI)
    
    # return a friendly error if a URI error is thrown 
    except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)

    # use a database named "CENG495HW1" and get collection named "items"
    db = client['CENG495HW1']
    return db
