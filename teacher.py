from flask_socketio import Namespace, emit
from flask import request, session
import clients


class TeacherNameSpace(Namespace):

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        clients.Teacher = [request.sid]
        emit('my_response', {'data': 'Teacher connected', 'count': 0})
        message = 'Teacher is connected, teacher sid {}'.format(clients.Teacher)
        emit('my_response', {'data': message, 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)
        clients.Teacher = []

    def on_action(self, action):
        action['count'] = session.get('receive_count', 0) + 1
        if action['type'] == 'my_ping':
            emit('my_pong')
        elif action['type'] == 'global_start_event' or action['type'] == 'global_pause_event':
            emit('action', action, broadcast=True, namespace='/student')
        elif action['type'] in ('student_pause_event', 'student_start_event'):
            if action['student_id'] in clients.Students:
                emit('action', action, room=clients.Students[action['student_id']], namespace='/student')