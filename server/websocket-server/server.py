# Adding path to libraries
import os
import sys

# Importing path to data analysis
from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import time
import json
import pandas as pd
from pumping_time_prediction import predict_pumping_time
import sched, time

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
  pumping_speed = data.get('value')
  duration = data.get('duration')
  client.publish('AT2018/Pumping', str(pumping_speed))
  time.sleep(duration)
  client.publish('AT2018/Pumping', 0)
  # time.sleep(delay_stop)
  # else:
  #   client.publish('AT2018/Pumping', str(pumping_speed))
  client.loop_stop()
  client.disconnect()

# Handling watering request. Getting request from webapp the publishing to the broker
@socketio.on('stop pumping')
def handle_stop_watering_request(data):
  print('Received data', str(data))
  print('Stop Pumping')
  broker = 'broker.hivemq.com'
  client = mqtt.Client(client_id="AT2018Client2")
  client.connect(broker)
  client.loop_start()
  pumping_speed = data.get('value')
  client.publish('AT2018/Pumping', str(pumping_speed))
  time.sleep(3)
  client.loop_stop()
  client.disconnect()


# Handling getting prediction from database event.
@socketio.on('get prediction from database')
def handle_getting_prediction_from_database():
  
  mongo_client = MongoClient('localhost', 27017)
  db = mongo_client.plant_monitoring
  collection = db.pumping_time_prediction
  data = collection.find().skip(collection.count() - 1)
  for record in data:
    duration = record.get('Duration')
    pumping_time = record.get('PredictionTime')

    json_data = {
      "pumpingTime": pumping_time,
      "duration": 0
    }
    socketio.emit('webapp prediction', json_data)
  mongo_client.close()

# Handling getting prediction from csvfile event.
@socketio.on('get demo data')
def handle_getting_demo_data_from_csvfile():
  demofile_path = os.path.join(os.path.dirname(__file__), '../data-analysis/data/output_demo.csv')  
  dataset = pd.read_csv(demofile_path, header = None).values
  n_samples = len(dataset)
  pumping_time_index, duration = predict_pumping_time(dataset)
  demo_data = [{
    'label': 'demo',
    'values': []
  }, {
    'label': 'point',
    'values': []
  }]

  for i in range (duration + 1):
    timesteps = int(pumping_time_index) + i
    demo_data[1]['values'].append({'x': timesteps, 'y': dataset.item(timesteps)})

  for i in range (n_samples):
    demo_data[0]['values'].append({'x': i, 'y': dataset.item(i)})

  socketio.emit('webapp demo data', {'demoData': demo_data})

if __name__ == '__main__':
  socketio.run(app, host = '0.0.0.0', port = 9001, debug = True)