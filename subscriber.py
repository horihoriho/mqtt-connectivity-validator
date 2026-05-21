# -*- coding: utf-8 -*-
import json
import logging

import paho.mqtt.client as mqtt

# Subscriver settings
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/sensor/temperature"

# Configure basic logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.FileHandler("./logs/subscriber.log"), logging.StreamHandler()],
)


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logging.info("Connected to MQTT broker")
        client.subscribe(TOPIC)
        logging.info(f"Subscribed to topic: {TOPIC}")
    else:
        logging.error(f"Failed to connect. reason_code={reason_code}")


def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
    except UnicodeDecodeError as e:
        logging.error(f"Failed to decode payload: {e}")
        return

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        logging.warning(f"Invalid JSON received: {payload}")
        return

    logging.info(
        f"Received data from {data['device_id']}: "
        f"Temperature: {data['temperature']}, "
        f"Humidity: {data['humidity']}, "
        f"Time: {data['timestamp']}"
    )


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()
