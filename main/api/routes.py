from flask import Blueprint, request, jsonify, session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .geojsonbuilder import buildgeojson
from . import classes


mod = Blueprint('api', __name__)

'''Live Scores'''
@mod.route('/live/soccer', methods=['GET'])
def updateLiveSoccer():
    ##To do:
    #Require Authentication.
    return buildgeojson({}, True, '')

'''Finished Games'''
@mod.route('/finished/soccer/<date>' , methods=['GET'])
def updateFinishedSoccer(date):
    ##To do:
    #Require Authentication.
    return buildgeojson({}, False, date)


##join chat room, establish connection and load all messages.
@socketio.on('join')
def join(message):
    if session.get('room'):
        leave_room(session['room'])
    session['room'] = message['match_id']
    print('entering:', session['room'])
    join_room(session['room'])
    

@socketio.on('leave')
def leave(message):
    room = session.get('room')
    session['room'] = ''
    print('leaving:', room)
    leave_room(room)


##Post Messages to db and emit to everyone in chat room.
@socketio.on('post_message')
def post_message(message):
    text = message['text']
    room = session['room']
    print(message)
    message = classes.Message(match_id = room, user = None, text= text)
    messages = classes.Messages(match_id = room)
    messages.postMessage(message = message)
    emit("load_message", [[{'text': message.text, 'date': message.date, 'time': message.time }]], room=room)


@mod.route('/messages/<match_id>', methods=['GET'])
def messages(match_id):
    messages = classes.Messages(match_id = match_id)
    return jsonify(messages.getMessages())