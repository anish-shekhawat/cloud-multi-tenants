from flask import session
from flask_socketio import emit, join_room, leave_room
from app import socketio
from flask_login import current_user

@socketio.on('connect')
def invited_connect():
    user_room = 'user_' + current_user.username
    # Join a custom user room
    join_room(user_room)
    #Emit a connected status message
    emit('status', {'data': 'Connected'})
    print('Client Conencted')

@socketio.on('disconnect')
def invited_disconnect():
    print('Client disconnected')
