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

key = "AAAA__ywlTk:APA91bF6MIcoPLpF4vPetYnky4FJAXgMRbwzVkvID-2iyoSaFIphSRarUTSnmQDvRKXLG3RLmfSUEYsHWEX7WKkXDCtPgEY5zQDk1FNC2lCUWnoMzwMQBwVrKtBeU_ay2Ta0zpZdnJQw"
headers = {
    "Content-Type": "application/json",
    "Authorization": "key={}".format(key)
}
server_key = '8jGerhqiOlLokORRMEx1WJqx0kCNqqXA'

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(payload_json):
    print(clients)
    payload = json.loads(payload_json)
    # requests.post('https://petandgo.herokuapp.com/api/mensajes', data=payload_json)
    if payload['receiver'] in clients.keys():
        print(clients[payload['receiver']])
        emit('message', payload_json, room=clients[payload['receiver']])
    else:
        r = requests.get(f"https://petandgo.herokuapp.com/api/usuarios/{payload['receiver']}/firebase", headers={"Authorization": server_key})
        if r.status_code == 200:
            data_raw = {
                "notification": {
                    "title": payload['sender'],
                    "body": payload['text']
                },
                "to": r.text
            }
            result = requests.post(fcmURL, headers=headers, data=json.dumps(data_raw))
            print(result)
    print(payload_json)
    emit('message', payload_json)


@socketio.on('join')
def join(email):
    clients[email] = request.sid


@socketio.on('connect')
def test_connect():
    print('connected')
    clients_test.append(request.sid)


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
    socketio.run(app)
