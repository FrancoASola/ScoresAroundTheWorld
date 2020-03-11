from flask import Blueprint
from .geojsonbuilder import buildgeojson

mod = Blueprint('api', __name__)

@mod.route('/live/soccer')
def updateLiveSoccer():
    #print('Updating GeoJson', current_matches)
    return buildgeojson({}, True, '')

@mod.route('/finished/soccer/<date>')
def updateFinishedSoccer(date):
    return buildgeojson({}, False, date)