# Set the path
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from application import create_app
from chat.views import socketio


app = create_app()
socketio.init_app(app, cors_allowed_origins="*")


if __name__ == "__main__":
    socketio.run(app)
