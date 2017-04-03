from flask_socketio import Namespace, emit
from flask import request, session
import clients


class TeacherNameSpace(Namespace):

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        clients.Teacher = [request.sid]
        emit('my_response', {'data': 'Teacher connected', 'count': 0})
        message = 'Teacher is in connected, teacher sid {}'.format(clients.Teacher)
        emit('my_response', {'data': message, 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)
        clients.Teacher = []

    def on_global_start_event(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('global_start_event', {'count': session['receive_count']}, broadcast=True, namespace='/student')

    def on_global_pause_event(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('global_pause_event', {'count': session['receive_count']}, broadcast=True, namespace='/student')

    def on_pause_student(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('student_pause_event', {'data': message['data'], 'count': session['receive_count']},
             room=clients.Students[message['data']], namespace='/student')

    def on_start_student(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('student_start_event', {'data': message['data'], 'count': session['receive_count']},
             room=clients.Students[message['data']], namespace='/student')
