from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from rooms.util import generate_room

rooms_app = Blueprint("rooms_app", __name__)


@rooms_app.route("/create_room", methods=["GET"])
def create_room():
    room_id = generate_room()
    data = {"room_id": room_id}
    return jsonify(data), 200


@rooms_app.route("/join_random", methods=["GET"])
def join_random():
    return jsonify({"room_id": "A1B2C3"}), 200


# @rooms_app.route("/chat")
@rooms_app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    username = data["username"]
    room = data["room"]
    # username= request.args.get('username')
    # room = request.args.get('room')
    if username and room:
        # return render_template("chat.html", username=username, room=room)
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error"})
