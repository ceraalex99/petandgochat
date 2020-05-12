from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import json
import requests

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


@socketio.on('message', namespace='/chat')
def handle_message(payload_json):
    payload = json.loads(payload_json)
    requests.post('https://petandgo.herokuapp.com/api/mensajes', data=payload_json)
    if clients[payload['receiver']]:
        emit('newMsg', payload_json, room=clients[payload['receiver']])
    else:
        data_raw = {
            "data": payload_json,
            "to": payload['receiver']
        }
        result = requests.post(fcmURL, headers=headers, data=json.dumps(data_raw))
        print(result)


@socketio.on('join', namespace='/chat')
def join(email):
    clients[email] = request.sid
    emit('joined', {'data': 'Lets dance'})


@socketio.on('connect', namespace='/chat')
def test_connect():
    clients_test.append(request.sid)
    emit('connect', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    clients_test.remove(request.sid)
    clients.pop(list(clients.keys())[list(clients.values()).index(request.sid)])


@socketio.on('my_event', namespace='/chat')
def test_message(message):
    emit('my_response', {'data': message['data']}, room=clients_test[0])


@socketio.on('my_event2', namespace='/chat')
def test_message3(message):
    emit('my_response', {'data': message['data']}, room=clients_test[1])


@socketio.on('my_broadcast_event', namespace='/chat')
def test_message2(message):
    emit('my_response', {'data': message['data']}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
