#!/usr/bin/env python
from flask import Flask, render_template
from student import StudentNameSpace
from teacher import TeacherNameSpace
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

Teacher = []
Students = {}

@app.route('/teacher')
def index():
    return render_template('teacher.html', async_mode=socketio.async_mode)


@app.route('/student')
def student():
    return render_template('student.html', async_mode=socketio.async_mode)

@app.route('/student2')
def student2():
    return render_template('student2.html', async_mode=socketio.async_mode)


socketio.on_namespace(TeacherNameSpace('/teacher'))
socketio.on_namespace(StudentNameSpace('/student'))


if __name__ == '__main__':
    socketio.run(app, host='10.131.167.168', debug=True)