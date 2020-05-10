from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

clients = []


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message', namespace='/chat')
def handleMessage(payloadJson):
    print("eoeoeoeo")
    payload = json.loads(payloadJson)
    requests.post('https://petandgo.herokuapp.com/api/mensajes', data=payloadJson)
    emit('newMsg', payloadJson, room=clients[payload['receiver']])
    emit('response', payloadJson)


@socketio.on('join', namespace='/chat')
def join(email):
    clients[email] = request.sid
    emit('after connect', {'data':'Lets dance'})


@socketio.on('connect', namespace='/chat')
def test_connect():
    print("connected")
    clients.append(request.sid)
    emit('my_response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    clients.remove(request.sid)
    print('Client disconnected')


@socketio.on('my_event', namespace='/chat')
def test_message(message):
    print("lol que funciona loko")
    emit('my_response', {'data': message['data']}, room=clients[0])


@socketio.on('my_event2', namespace='/chat')
def test_message3(message):
    print("lol que funciona loko2")
    emit('my_response', {'data': message['data']}, room=clients[1])


@socketio.on('my_broadcast_event', namespace='/chat')
def test_message2(message):
    emit('my_response', {'data': message['data']}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
