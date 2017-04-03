from flask import session
from flask_socketio import Namespace, emit
from flask import request
import clients


class StudentNameSpace(Namespace):

    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        #Saves student_id and session id to dict
        clients.Students[message['data']] = request.sid
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        message = {'data': 'student_id1'}
        emit('my_response',
             {'data': 'Student connected {}, sudent_id {}'.format(request.sid, message['data']), 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)

    def on_action(self, action):
        if action['type'] == 'my_ping':
            emit('action', {'type': 'my_pong'})
        elif action['type'] == 'ask_help_event':
            if len(clients.Teacher):
                action['count'] = session.get('receive_count', 0) + 1
                emit('action', action, room=clients.Teacher[0], namespace='/teacher')
            else:
                emit('action', {'message': 'Teacher is disconnected'})
        elif action['type'] == 'register':
            clients.Students[action['student_id']] = request.sid

    def on_ask_help_event(self, message):
        if len(clients.Teacher):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_response', {'data': 'I"m asking for helpIN ROOM {} '.format(clients.Teacher)})
            emit('ask_help_event', {'data': message['data'], 'count': session['receive_count']},
                 room=clients.Teacher[0], namespace='/teacher')
        else:
            emit('my_response', {'data': 'Teacher is disconnected'})