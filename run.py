import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from main import create_app, socketio

app = create_app(config_object = 'main.settings')

if __name__ == '__main__':
    socketio.run(app)