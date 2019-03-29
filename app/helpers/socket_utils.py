import functools
import flask

from flask_jwt_extended import current_user
from flask_socketio import emit, join_room, leave_room, send
from app import app, socketio, db
from app.account.user.authenticated.models import AccountUserAuthenticated
from app.account.user.models import AccountUser


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('my event')
@authenticated_only
def handle_my_custom_event(data):
    user = AccountUser.get_current_user()
    emit('my response', {'message': '{0} has joined'.format(user.name)}, broadcast=True)


@socketio.on('my event', namespace='/notification')
def my_event(msg):
    user = AccountUser.get_by_id(msg['data'])
    session = AccountUserAuthenticated.get_by_user_id(user.id)
    if session:
        session.delete()
        session.save()
    else:
        db.session.add((AccountUserAuthenticated(user.id, flask.request.sid)))
        db.session.commit()
    data = {'message': '{0} is online'.format(user.get_full_name()), 'status': 'connect', 'id': user.id}
    socketio.emit('connection response', data, namespace='/notification')
    app.logger.info('Connection established by {}'.format(msg['data']))
    online_users_data = AccountUser.get_online_users()
    socketio.emit('online users', online_users_data, namespace='/notification')


@socketio.on('user disconnect')
def user_disconnect(msg):
    app.logger.info('{} disconnected'.format(msg['data']))


@socketio.on('connect', namespace='/notification')
def connect_handler():
    app.logger.info("Client connecting...")


@socketio.on('disconnect', namespace='/notification')
def disconnect():
    app.logger.info("Client disconnecting...")
    session = AccountUserAuthenticated.get_by_session_id(flask.request.sid)
    session.delete()
    session.save()
    online_users_data = AccountUser.get_online_users()
    socketio.emit('online users', online_users_data, namespace='/notification')
    app.logger.info("Socket sent a message to notification namespace")


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    app.logger.error(e, exc_info=True)


@socketio.on_error('/notification')  # handles the '/notification' namespace
def error_handler_notification(e):
    app.logger.error(e, exc_info=True)


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    app.logger.error(e, exc_info=True)


@socketio.on('join', namespace='/notification')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room=room, namespace='/notification')
    send(username + ' has entered the room.', room=room)
    app.logger.info(username + ' has entered the room.')


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


def emit_notification(event, message, status):
    data = {
        "message": "{0}".format(message),
        "event": "{0}".format(event),
        "status": "{0}".format(status)
    }
    socketio.emit('message', data, namespace='/notification')
