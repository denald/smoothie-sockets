from flask import session
from flask_socketio import Namespace, emit, join_room
from flask import request
import example.clients


class StudentNameSpace(Namespace):

    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        #Saves student_id and session id to dict
        example.clients.Students[message['data']] = request.sid
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        message = {}
        message['data'] = 'student_id1'
        emit('my_response',
             {'data': 'Student connected {}, sudent_id {}'.format(request.sid, message['data']), 'count': 0})
        # example.clients.Students[message['data']] = request.sid

    def on_disconnect(self):
        print('Client disconnected', request.sid)

    def on_ask_help_event(self, message):
        if len(example.clients.Teacher):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response', {'data': 'I"m asking for helpIN ROOM {} '.format(example.clients.Teacher)})
            emit('ask_help_event', {'data': message['data'], 'count': session['receive_count']},
                 room=example.clients.Teacher[0], namespace='/teacher')
        else:
            emit('my_response', {'data': 'Teacher is disconnected'})