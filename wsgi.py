# Set the path
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from application import create_app
from application import socketio


app = create_app()

if __name__ == "__main__":
    app.run()
