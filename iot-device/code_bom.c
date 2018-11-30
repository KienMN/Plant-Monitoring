#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define MOTOR1 D1
#define MOTOR2 D3
#define DHTPIN D2
#define DHTTYPE  DHT11
#define ONE_WIRE_BUS D2
#define DHT_DELAY 2
#define SEND_TIME 5
#define PUMPING_PUBLISH_RATE 1

const char* ssid = "access point";
const char* password = "passwork";
const char* mqtt_server = "broker.hivemq.com";
const char* device_id = "AT2018_Device";
char pumpState = 0;

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

float temperature;
float humidity;

unsigned long previousMillis = 0;
unsigned long lastSend = 0;

void readSensors() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= DHT_DELAY * 1000)
  {
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    previousMillis = currentMillis;
  }
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");

    if (client.connect(device_id)) {
      Serial.println("connected");
      client.subscribe("AT2018/Pumping");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println("try again in 5 seconds");
      delay(500);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0';
  if (strcmp(topic, "AT2018/Pumping") == 0) {
    analogWrite(MOTOR1, atoi((char*)payload));
    digitalWrite(MOTOR2, 0);
    if(atoi((char*)payload) != 0) {
			pumpState = 1;
		} else {
			pumpState = 0;
		}
  }
}

void sendMQTT() {
  readSensors();
  unsigned long nowSend = millis();
  if (pumpState == 1) {
    if ((nowSend - lastSend) % (PUMPING_PUBLISH_RATE * 1000) == 0) {
      char msg[10];
      snprintf(msg, 10, "%d", pumpState);
      client.publish("AT2018/PumpingStatus", msg);
    }
  } else {
    if (nowSend -  lastSend > SEND_TIME * 1000) {
      char msg[10];
      snprintf(msg, 10, "%d", pumpState);
      client.publish("AT2018/PumpingStatus", msg);
    }
  }

  if (nowSend -  lastSend > SEND_TIME * 1000) {
    char msg[10];
    snprintf (msg, 10, "%d", (int)temperature);
    client.publish("AT2018/Temperature", msg);
    snprintf (msg, 10, "%d", (int)humidity);
    client.publish("AT2018/Humidity", msg);
    snprintf(msg, 10, "%d", analogRead(A0));
    client.publish("AT2018/SoilMoisture", msg);
    lastSend = nowSend;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(D1, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D6, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  sendMQTT();
}
