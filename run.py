from main import create_app, socketio

app = create_app(config_object = 'main.settings')

if __name__ == '__main__':
    socketio.run(app)