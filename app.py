from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from pymongo import MongoClient
from uuid import uuid4
app = Flask(__name__)

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client['chatapp']
users_collection = db['users']
users_collection.create_index('username', unique=True)
chats_collection = db['chat']
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def hello():
    return render_template("index.html")
    # return 'hello world'

@app.route("/", methods=["POST"])
def signin():
    username = request.args.get('username')
    password = request.args.get('password')
    if username and password:
        existing_data = users_collection.find_one({"username" : username})
        if existing_data:
            return render_template("select.html", username=username)
        else:
            users_collection.insert_one({"username" : username, "password" : password})
            return render_template("select.html", username=username)
    return render_template("index.html")
        
    
@app.route("/chat")
# @app.route("/chat", methods=["POST"])
def chat():
    # data = request.json
    # username = data['username']
    # room = data['room']
    username= request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template("chat.html", username=username, room=room)
        # return jsonify({"status" : "success"})
    else:
        return jsonify({"status" : "error"})

@socketio.on("connect")
def socket_connect():
    print("connected")
    
    
@socketio.on('join_room')
def handle_join_room_event(data):
    auth = request.headers.get('Authorization')
    token = auth.split(' ')[1]
    print(token)
    print(f"{data['username']} has joined the room {data['room']}")
    print(type(data))
    join_room(data['room'])
    chats = db[data['room']].find({})
    c = []
    for chat in chats:
        print(chat)
        c.append(chat)
    
    dat = {"chats" : c}
    
    print(type(dat))
    socketio.emit('join_room_announcement',dat )

@socketio.on('send_message')
def handle_send_message_event(data):
    print(f"message from {data['username']} in the room {data['room']}: {data['message']}")
    try:
        db[data['room']].insert_one({'_id':uuid4().hex,'username':data['username'],'message':data['message']})
    except Exception as e:
        print(e)
    print("triggering receivemessage")
    socketio.emit('receive_message', data, room=data['room'])   


if __name__ == '__main__':
    socketio.run(app,debug=True, port=5000)