import ssl
import json
import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime

# ⚙️ Configuración
ENDPOINT = "a32w8s71hfr88r-ats.iot.us-east-1.amazonaws.com"
PORT = 8883
TOPIC = "iot/data"

# Certificados
CA_PATH = "certificados/AmazonRootCA1.pem"
CERT_PATH = "certificados/device-certificate.pem.crt"
KEY_PATH = "certificados/device-private.pem.key"

# Configurar cliente MQTT
client = mqtt.Client()

client.tls_set(ca_certs=CA_PATH,
               certfile=CERT_PATH,
               keyfile=KEY_PATH,
               tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers=None)

def on_connect(client, userdata, flags, rc):
    print("Conectado con código:", rc)
    if rc == 0:
        # Generar datos aleatorios
        device_id = f"{random.randint(1, 10):04d}"  # ID entre 1-10 como "0001", "0002", etc.
        timestamp = datetime.now().isoformat()
        temperature = round(random.uniform(10, 30), 2)
        humidity = round(random.uniform(30, 90), 2)
        valve_state = random.choice(["on", "off"])

        payload = {
            "device_id": device_id,
            "date": timestamp,
            "temperature": temperature,
            "humidity": humidity,
            "valve_state": valve_state
        }

        client.publish(TOPIC, json.dumps(payload), qos=1)
        print("Mensaje enviado al tópico:", TOPIC)
        time.sleep(2)
        client.disconnect()
    else:
        print("Error al conectar")

client.on_connect = on_connect

# 🔌 Conectarse y arrancar
print("Conectando a AWS IoT...")
client.connect(ENDPOINT, PORT)
client.loop_forever()