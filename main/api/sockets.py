from flask_socketio import emit, join_room, leave_room
from .. import socketio
from flask import session

##Leave chat currently in (if any) and join chat room.
@socketio.on('join')
def join(message):
    if session.get('room'):
        leave_room(session['room'])
    session['room'] = message['match_id']
    print('entering:', session['room'])
    join_room(session['room'])
    
##Leave chat room
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
    message = classes.Message(match_id = room, user = None, text= text)
    messages = classes.Messages(match_id = room)
    messages.postMessage(message = message)
    emit("load_message", [[{'text': message.text, 'date': message.date, 'time': message.time }]], room=room)

