import requests
from flask import Flask, session, render_template, request
from flask_session import Session
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import geojsonbuilder

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

current_matches = {}

@app.route('/')
def index():
    '''Main Page'''
    print('STARTING UP')
    geojsonbuilder.buildgeojson(current_matches)
    return render_template('index.html')

def updategeojson():
    print('Updating GeoJson', current_matches)
    geojsonbuilder.buildgeojson(current_matches)

sched = BackgroundScheduler(daemon=True)
sched.add_job(updategeojson, 'interval', seconds = 60)
sched.start()