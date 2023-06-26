
import string
import secrets
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client['chatapp']
rooms = db['rooms']
def generate_room():
    characters = string.ascii_uppercase + string.digits
    room = ''.join(secrets.choice(characters) for i in range(6))
    room_exists = rooms.find_one({"room":room})
    if room_exists:
        generate_room()
    # rooms.insert_one({"room":room})
    return room

