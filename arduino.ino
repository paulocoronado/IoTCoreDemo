#include <ESP8266WiFi.h>
#include <WiFiClientSecureBearSSL.h>
#include <PubSubClient.h>
#include <DHT.h>
#include "certs.h"  // Tu archivo con certificados como cadenas de texto

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// WiFi
const char* ssid = "TU_SSID";
const char* password = "TU_PASSWORD";

// AWS IoT
const char* mqtt_server = "xxxxxxx-ats.iot.us-east-1.amazonaws.com";
const int mqtt_port = 8883;
const char* mqtt_topic = "iot/data";

// Cliente SSL
BearSSL::WiFiClientSecure net;
PubSubClient client(net);

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi conectado");
}

void connectMQTT() {
  static BearSSL::X509List ca(AWS_ROOT_CA);
  static BearSSL::X509List client_crt(DEVICE_CERT);
  static BearSSL::PrivateKey client_key(PRIVATE_KEY);

  net.setTrustAnchors(&ca);
  net.setClientRSACert(&client_crt, &client_key);

  client.setServer(mqtt_server, mqtt_port);

  while (!client.connected()) {
    if (client.connect("ESP8266Client")) {
      Serial.println("Conectado a AWS IoT");
    } else {
      Serial.print(".");
      delay(1000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  connectWiFi();
  connectMQTT();
}

void loop() {
  if (!client.connected()) {
    connectMQTT();
  }

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (!isnan(h) && !isnan(t)) {
    String payload = "{";
    payload += "\"device_id\":\"0001\",";
    payload += "\"temperature\":" + String(t, 2) + ",";
    payload += "\"humidity\":" + String(h, 2);
    payload += "}";

    client.publish(mqtt_topic, payload.c_str());
    Serial.println("Payload enviado:");
    Serial.println(payload);
  }

  delay(10000);
}