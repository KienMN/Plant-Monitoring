import paho.mqtt.client as mqtt
import time
from socketIO_client import SocketIO

broker = 'broker.hivemq.com'

def on_log(client, userdata, level, buff):
  print('Log', buff)

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connected")
    client.subscribe('AT2018/Temperature')
    client.subscribe('AT2018/Humidity')
    client.subscribe('AT2018/SoilMoisture')
  else:
    print("Bad connection. Returned code", rc)

def on_disconnect(client, userdata, flags, rc = 0):
  print("Disconnected with returned code", rc)

def on_message(client, userdata, msg):
  topic = msg.topic
  message = str(msg.payload.decode('UTF-8'))
  print(topic, message)
  with SocketIO('localhost', 9001) as socketio:
    socketio.emit('my event', {'topic': topic, 'message': message})

client = mqtt.Client(client_id='testtttt3')
# client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print('Connecting to broker', broker)

client.connect(broker)
client.loop_forever()