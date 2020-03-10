from flask import Blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from .geojsonbuilder import buildgeojson

mod = Blueprint('api', __name__)

@mod.route('/soccer')
def updategeojson():
    #print('Updating GeoJson', current_matches)
    return buildgeojson({})
