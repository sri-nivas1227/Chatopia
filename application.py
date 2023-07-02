from flask import Flask
from flask_cors import CORS


def create_app(**config_overrides):
    app = Flask(__name__)
    # load config
    app.config.from_pyfile("settings.py")
    # apply overrides for tests
    app.config.update(config_overrides)
    # import blueprints and register them

    ## authentication blueprint
    from authentication.views import auth_app

    app.register_blueprint(auth_app)
    ## rooms blueprint
    from rooms.views import rooms_app

    app.register_blueprint(rooms_app)
    ## chat blueprint
    from chat.views import chat_app, socketio

    app.register_blueprint(chat_app)
    socketio.init_app(app, cors_allowed_origins="*")

    # enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # return the app
    return app
