# Adding path to libraries
import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data-analysis')))

# Importing path to data analysis
from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import paho.mqtt.client as mqtt
import time
import json
import pandas as pd
from pumping_time_prediction import predict_pumping_time
# from data-analysis
# from data-analysis.

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

# Handling getting prediction from database event.
@socketio.on('get prediction from database')
def handle_getting_prediction_from_database():
  
  mongo_client = MongoClient('localhost', 27017)
  db = mongo_client.plant_monitoring
  collection = db.pumping_time_prediction
  data = collection.find().skip(collection.count() - 1)
  for record in data:
    duration = record.get('Duration')

    if duration < 0:
      pumping_time = "You do not need to water"
    else:
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
  # input_filepath = os.path.join(os.path.dirname(__file__), '../data/input_demo.csv')
  output_filepath = os.path.join(os.path.dirname(__file__), '../data-analysis/data/output_demo.csv')
  demofile_path = os.path.join(os.path.dirname(__file__), '../data-analysis/data/output_demo.csv')
  
  dataset = pd.read_csv(output_filepath, header = None).values
  n_samples = len(dataset)

  pumping_time_index, duration = predict_pumping_time(dataset)

  print(pumping_time_index, duration)

  # print(dataset)
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