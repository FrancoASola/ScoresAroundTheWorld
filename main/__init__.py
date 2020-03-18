from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(config_object = 'main.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.debug = True
    
    from .extensions import mongo
    mongo.init_app(app)

    from main.site.routes import mod
    app.register_blueprint(site.routes.mod)

    from main.api.routes import mod
    app.register_blueprint(api.routes.mod, url_prefix ='/api')

    socketio.init_app(app)

    return app