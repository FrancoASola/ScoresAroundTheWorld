from flask_socketio import emit, join_room, leave_room
from .. import socketio
from flask import session
from . import classes

##Leave current chat (if any) and join chat room.
@socketio.on('join')
def join(message):
    #Message Room
    if session.get('msg_room'):
        leave_room(session['msg_room'])
    session['msg_room'] = message['match_id']
    join_room(session['msg_room'])

    #Highlight Room
    if session.get('hl_room'):
        leave_room(session['hl_room'])
    session['hl_room'] = f"{message['match_id']}_hl"
    join_room(session['hl_room'])

##Leave chat msg_room
@socketio.on('leave')
def leave(message):
    #Message Room
    msg_room = session.get('msg_room')
    session['msg_room'] = ''
    leave_room(msg_room)

    #Highlight Room
    hl_room = session.get('hl_room')
    session['hl_room'] = ''
    leave_room(hl_room)

##Post Messages to db and emit to everyone in chat msg_room.
@socketio.on('post_message')
def post_message(message):
    text = message['text']
    msg_room = session['msg_room']
    message = classes.Message(match_id = msg_room, user = None, text= text)
    messages = classes.Messages(match_id = msg_room)
    messages.postMessage(message = message)
    emit("load_message", [[{'text': message.text, 'date': message.date, 'time': message.time }]], room=msg_room)

##Post highlights to db and emit to everyone in chat hl_room
@socketio.on('post_higlight')
def post_highlights(message):
    url = message['url']
    title = message['title']
    hl_room = session['hl_room']
    highlight = classes.Highlight(match_id = hl_room, user = None, url= url, title=title)
    highlights =  classes.Highlights(match_id = hl_room)
    highlights.postHighlight(message = message)
    emit('load_highlights', [[{'url' : highlight.url, 'title': highlight.url, 'date': highlight.date, 'time': highlight.time}]], room=hl_room)
