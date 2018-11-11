import paho.mqtt.client as mqtt
import time
from socketIO_client import SocketIO
import datetime
from pymongo import MongoClient

broker = 'broker.hivemq.com'
record = {}

def on_log(client, userdata, level, buff):
  print('Log', buff)

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connected")
    client.subscribe('AT2018/Temperature')
    client.subscribe('AT2018/Humidity')
    client.subscribe('AT2018/SoilMoisture')
    client.subscribe('AT2018/LightIntensity')
    client.subscribe('AT2018/PumpingStatus')
  else:
    print("Bad connection. Returned code", rc)

def on_disconnect(client, userdata, flags, rc = 0):
  print("Disconnected with returned code", rc)

def on_message(client, userdata, msg):
  # Getting data from broker
  topic = msg.topic
  message = str(msg.payload.decode('UTF-8'))
  # print(topic, message)
  ts = time.localtime()
  date_and_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)
  # print(date_and_time)
  global record
  record["Timestamp"] = date_and_time
  if topic == 'AT2018/Temperature':
    record["Temperature"] = message
  elif topic == 'AT2018/Humidity':
    record["Humidity"] = message
  elif topic == 'AT2018/SoilMoisture':
    v = int(message)
    v = (1024 - v) * 100 // 1024
    message = str(v)
    record["SoilMoisture"] = message
  elif topic == 'AT2018/LightIntensity':
    v = int(message)
    v = 1024 - v
    message = str(v)
    record["LightIntensity"] = message
  elif topic == 'AT2018/PumpingStatus':
    record["PumpingStatus"] = message
  if (len(record) == 6):
    print(record)
    # mongo_client = MongoClient('localhost', 27017)
    # db = mongo_client.plant_monitoring
    # collection = db.sensor_data
    # collection.insert_one(record)
    record = {}

  # Emitting data to websocket server
  with SocketIO('localhost', 9001) as socketio:
    socketio.emit('monitoring', {'topic': topic, 'message': message})

client = mqtt.Client(client_id='testtttt1')
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print('Connecting to broker', broker)

client.connect(broker)
client.loop_forever()