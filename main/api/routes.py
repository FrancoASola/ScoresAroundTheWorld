from flask import Blueprint
from .geojsonbuilder import buildgeojson

mod = Blueprint('api', __name__)

@mod.route('/live/soccer', methods=['GET'])
def updateLiveSoccer():
    ##To do:
    #Require Authentication. Maybe logging in?
    return buildgeojson({}, True, '')

@mod.route('/finished/soccer/<date>' , methods=['GET'])
def updateFinishedSoccer(date):
    ##To do:
    #Require Authentication. Maybe logging in?
    return buildgeojson({}, False, date)