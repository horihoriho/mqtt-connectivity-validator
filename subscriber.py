# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

# Subscriver settings
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/sensor/temperature"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect. reason_code={reason_code}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Received message: topic={message.topic}, payload={payload}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()
