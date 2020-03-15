from flask import Blueprint, request, jsonify
from .geojsonbuilder import buildgeojson
from . import classes


mod = Blueprint('api', __name__)

@mod.route('/live/soccer', methods=['GET'])
def updateLiveSoccer():
    ##To do:
    #Require Authentication.
    return buildgeojson({}, True, '')

@mod.route('/finished/soccer/<date>' , methods=['GET'])
def updateFinishedSoccer(date):
    ##To do:
    #Require Authentication.
    return buildgeojson({}, False, date)

@mod.route('/messages/<match_id>', methods=['POST'])
def post_message(match_id):
    ##To do:
    #Ruire Log in
    text = request.form['text']
    message = classes.Message(match_id = match_id, user = None, text= text)
    messages = classes.Messages(match_id = match_id)
    messages.postMessage(message = message)
    return messages.getMessages()

@mod.route('/messages/<match_id>', methods=['GET'])
def messages(match_id):
    print('getting messages')
    messages = classes.Messages(match_id = match_id)
    
    return jsonify(messages.getMessages())