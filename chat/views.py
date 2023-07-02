from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask import Blueprint
from uuid import uuid4
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGODB_HOST"), os.getenv("MONGODB_PORT"))
db = mongo_client["chatapp"]
chats = db["chat"]

chat_app = Blueprint("chat_app", __name__)

socketio = SocketIO()


@socketio.on("connect")
def socket_connect():
    print("connected")


@socketio.on("join_room")
def handle_join_room_event(data):
    # auth = request.headers.get('Authorization')
    # token = auth.split(' ')[1]
    # print(token)
    print(f"{data['username']} has joined the room {data['room_id']}")
    print(type(data))
    join_room(data["room_id"])
    chats = db[data["room_id"]].find({})
    c = []
    for chat in chats:
        print(chat)
        c.append(chat)
    dat = {"chats": c}

    print(type(dat))
    socketio.emit("join_room_announcement", dat)


@socketio.on("send_message")
def handle_send_message_event(data):
    print(
        f"message from {data['username']} in the room {data['room']}: {data['message']}"
    )
    try:
        db[data["room"]].insert_one(
            {
                "_id": uuid4().hex,
                "username": data["username"],
                "message": data["message"],
            }
        )
    except Exception as e:
        print(e)
    print("triggering receivemessage")
    socketio.emit("receive_message", data, room=data["room"])
