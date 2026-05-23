# -*- coding: utf-8 -*-
import json
import logging
from pathlib import Path

import paho.mqtt.client as mqtt

# Subscriber settings
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/sensor/temperature"

Path("logs").mkdir(exist_ok=True)

# Configure basic logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("./logs/subscriber.log"), logging.StreamHandler()],
)


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logging.info("Connected to MQTT broker.")
        client.subscribe(TOPIC)
        logging.info(f"Subscribed to topic: {TOPIC}")
    else:
        logging.error(f"Failed to connect. reason_code={reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    if reason_code == 0:
        logging.info("Disconnected from MQTT broker.")
    else:
        logging.warning(
            f"Unexpected disconnection from MQTT broker. reason_code={reason_code}"
        )


def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
    except UnicodeDecodeError as error:
        logging.warning(f"Failed to decode payload: {error}")
        return

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        logging.warning(f"Invalid JSON received: {payload}")
        return

    if not isinstance(data, dict):
        logging.warning(
            "Invalid data format. Expected JSON object, "
            f"got {type(data).__name__}: {data}"
        )
        return

    required_keys = ["device_id", "temperature", "humidity", "timestamp"]

    for key in required_keys:
        if key not in data:
            logging.warning(f"Missing required key: {key}. data={data}")
            return
    try:
        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]
        timestamp = data["timestamp"]

        if not isinstance(device_id, str):
            raise TypeError("device_id must be a string.")
        if not isinstance(temperature, (int, float)):
            raise TypeError("temperature must be a number")
        if not isinstance(humidity, (int, float)):
            raise TypeError("humidity must be a number")
        if not isinstance(timestamp, str):
            raise TypeError("timestamp must be a string")

    except TypeError as error:
        logging.warning(f"Invalid data type: {error}. data={data}")
        return

    logging.info(
        f"Received data from {device_id}: "
        f"temperature={temperature}, "
        f"humidity={humidity}, "
        f"time={timestamp}"
    )


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()
