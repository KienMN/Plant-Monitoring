#include <ESP8266WiFi.h>
#include <PubSubClient.h>


#define SEND_TIME 5

const char* ssid = "access point";
const char* password = "passwork";
const char* mqtt_server = "broker.hivemq.com";
const char* device_id = "AT2018_LightSensor";


WiFiClient espClient;
PubSubClient client(espClient);

float lightIntensity;

unsigned long previousMillis = 0;
unsigned long lastSend = 0;


void setup_wifi()
{
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect()
{
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");

    if (client.connect(device_id))
    {
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println("try again in 5 seconds");
      delay(500);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length)
{
  payload[length] = '\0';
}

void sendMQTT()
{
  unsigned long nowSend = millis();
  if (nowSend -  lastSend > SEND_TIME * 1000)
  {
    char msg[10];
    snprintf(msg, 10, "%d", analogRead(A0));
    client.publish("AT2018/LightIntensity", msg);
    lastSend = nowSend;
  }
}

void setup()
{
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop()
{
  if (!client.connected())
    {
        reconnect();
    }
    client.loop();
    sendMQTT();
}
