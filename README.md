# Applying IoT solution for Plant monitoring

Project provides codes for IoT devices, MQTT protocol, WebSocket server and Machine learning in order to monitor and analyse plant data.

## Getting Started

### Folders structure
```
iot-device: Codes for IoT devices.
server/data-analysis: Data, models and codes for sata analysing.
server/mqtt-client: Mqtt client which subscribes to topic published by the devices.
server/websocket-server: Websocket server which maintains real time connection with mqtt client and web application.
web-app: React app for user interface.
```
### Prerequisites

#### Server

Necessary package

```
numpy
pandas
matplotlib
sklearn
keras
tensorflow
paho-mqtt
flask_socketio
socketIO-client
pymongo
```

#### Web application

Dependencies can be found in package.json file.

### Installing

#### Server

In server directory, creating a virtual environment for deploying server:
```
virtualenv env -p python3
```

Activating virtual environment:
```
source env/bin/activate
```

Installing dependencies:
```
pip install {package}
```

Running mqtt subcribe node:
```
python mqtt-client/client-subscribe.py
```

Running web socket server:
```
python websocket-server/server.py
```

#### Web application
In web-app directory, installing dependencies for deploying web application
```
npm install
```

Starting web application
```
npm start
```

Starting script can be found in package.json file.

## Deployment
When deploying in a real server, PM2 is a good choice for managing process.