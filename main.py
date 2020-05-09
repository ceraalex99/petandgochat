from flask import Flask, request
from flask_socketio import SocketIO, emit
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

clients = {}


@app.route('/')
def index():
    return 'Hello'

@socketio.on('message')
def handleMessage(payloadJson):
    payload = json.loads(payloadJson)
    requests.post('https://petandgo.herokuapp.com/api/mensajes', data=payloadJson)
    emit('newMsg', payloadJson, room=clients[payload['receiver']])


@socketio.on('join')
def join(email):
    clients[email] = request.sid


if __name__ == '__main__':
    socketio.run(app)
