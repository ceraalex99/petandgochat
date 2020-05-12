from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import json
import logging
import requests

logging.basicConfig(level=logging.NOTSET)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

clients_test = []
clients = {}


fcmURL = "https://fcm.googleapis.com/fcm/send"

key = "AIzaSyBHx4y44Mxlf1Ucy3dVX4IGux-OWCc46No"
headers = {
    "Content-Type": "application/json",
    "Authorization": "key={}".format(key)
}


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(payload_json):
    payload = json.loads(payload_json)
    # requests.post('https://petandgo.herokuapp.com/api/mensajes', data=payload_json)
    # if clients[payload['receiver']]:
    #     emit('newMsg', payload_json, room=clients[payload['receiver']])
    # else:
    #     data_raw = {
    #         "data": payload_json,
    #         "to": payload['receiver']
    #     }
    #     result = requests.post(fcmURL, headers=headers, data=json.dumps(data_raw))
    #     print(result)
    print(payload_json)
    emit('message', payload_json)

@socketio.on('join')
def join(email):
    clients[email] = request.sid
    emit('joined', {'data': 'Lets dance'})


@socketio.on('connect')
def test_connect():
    print('connected')
    clients_test.append(request.sid)
    emit('connect', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    clients_test.remove(request.sid)
    clients.pop(list(clients.keys())[list(clients.values()).index(request.sid)])


@socketio.on('my_event')
def test_message(message):
    emit('my_response', {'data': message['data']}, room=clients_test[0])


@socketio.on('my_event2')
def test_message3(message):
    emit('my_response', {'data': message['data']}, room=clients_test[1])


@socketio.on('my_broadcast_event')
def test_message2(message):
    emit('message', {'data': message['data']}, broadcast=True)


if __name__ == '__main__':
    print("hola")
    socketio.run(app)
