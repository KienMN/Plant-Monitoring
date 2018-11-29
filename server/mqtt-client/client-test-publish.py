import paho.mqtt.client as mqtt
import time

broker = 'broker.hivemq.com'

def on_log(client, userdata, level, buff):
  print('Log', buff)

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connected")
  else:
    print("Bad connection. Returned code", rc)

def on_disconnect(client, userdata, flags, rc = 0):
  print("Disconnected with returned code", rc)

def on_message(client, userdata, msg):
  topic = msg.topic
  message = str(msg.payload)
  print(topic, message)

client = mqtt.Client(client_id='testtttt2')
# client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print('Connecting to broker', broker)
client.connect(broker)
i = 1
while(True):
  client.loop_start()
  client.publish('AT2018/Temperature', str(i).encode('UTF-8'))
  client.publish('AT2018/Humidity', str(i).encode('UTF-8'))
  client.publish('AT2018/SoilMoisture', str(i).encode('UTF-8'))
  client.publish('AT2018/LightIntensity', str(i).encode('UTF-8'))
  # client.publish('AT2018/PumpingStatus', str(i).encode('UTF-8'))
  time.sleep(20)
  client.loop_stop()
  i += 1
client.disconnect()