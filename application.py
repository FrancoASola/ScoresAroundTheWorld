import os
import requests
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    '''Main Page'''
    return render_template('index.html')

@app.route('/map.geojson')
def map_pull():
    return {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-68.115234375,-35.88905007936092]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-68.31298828125,-34.58799745550482]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[2.109375,41.47566020027821]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-3.69140625,40.43022363450862]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[4.306640625,45.82879925192134]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-8.5693359375,41.1455697310095]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-0.15380859375,51.56341232867588]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-3.01025390625,53.461890432859114]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[4.9658203125,52.44261787120725]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[11.57958984375,48.1367666796927]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[9.16259765625,45.49094569262732]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[12.5244140625,41.902277040963696]}},{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[14.30419921875,40.88029480552824]}}]}