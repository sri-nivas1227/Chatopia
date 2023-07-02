from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGODB_HOST"), int(os.getenv("MONGODB_PORT")))
db = mongo_client["chatapp"]
profile = db["profile"]

auth_app = Blueprint("auth_app", __name__)


@auth_app.route("/login", methods=["POST"])
def handle_login():
    data = request.json
    username = data["username"]
    password = data["password"]
    if username and password:
        if_user = profile.find_one({"username": username})
        if if_user:
            if if_user["password"] == password:
                return jsonify({"status": "success"}), 200
            else:
                return jsonify({"status": "error"}), 400
        else:
            profile.insert_one({"username": username, "password": password})
            return jsonify({"status": "success"}), 200
