from flask import Flask
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import time
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Handling monitoring event. Getting data from sensors through mqtt client subscribe
@socketio.on('monitoring')
def handle_monitoring(json):
  print('Received data', str(json))
  socketio.emit('webapp monitoring', json)

# Handling watering request. Getting request from webapp the publishing to the broker
@socketio.on('pumping')
def handle_water_request(data):
  print('Received data', str(data))
  print('Pumping')
  broker = 'broker.hivemq.com'
  client = mqtt.Client(client_id="AT2018Client2")
  client.connect(broker)
  client.loop_start()
  client.publish('AT2018/Pumping', str(data.get("value")).encode('UTF-8'))
  time.sleep(5)
  client.loop_stop()
  client.disconnect()

if __name__ == '__main__':
  socketio.run(app, host = '0.0.0.0', port = 9001, debug = True)