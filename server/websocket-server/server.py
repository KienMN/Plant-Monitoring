from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('my event')
def handle_my_event(json):
  print('Received data', str(json))
  socketio.emit('send data', json)

if __name__ == '__main__':
  socketio.run(app, host = '0.0.0.0', port = 9001, debug = True)