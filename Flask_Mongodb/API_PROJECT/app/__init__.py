from flask import Flask
from flask_pymongo import PyMongo
from config import Config


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config["MONGO_URI"] = Config.MONGO_URI
mongo = PyMongo(app)
db = mongo.db
collection = mongo.db["Interfaces"]


from app import homepage_route, interface_routes, errors
