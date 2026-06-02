# -*- coding: utf-8 -*-

import json
import random
import time
from datetime import datetime
import logging
from pathlib import Path

import paho.mqtt.client as mqtt

# Publisher settings
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/sensor/temperature"
PUBLISH_INTERVAL_SECONDS = 3

Path("logs").mkdir(exist_ok=True)

# Configure basic logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("./logs/publisher.log"), logging.StreamHandler()],
)


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logging.info("Connected to MQTT broker.")
    else:
        logging.error(f"Failed to connect. reason_code={reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    if reason_code == 0:
        logging.info("Disconnected from MQTT broker.")
    else:
        logging.warning(
            f"Unexpected disconnection from MQTT broker. reason_code={reason_code}"
        )


def create_sensor_data():
    return {
        "device_id": "sensor-001",
        "temperature": round(random.uniform(20.0, 30.0), 1),
        "humidity": random.randint(40, 70),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
        client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    except ConnectionRefusedError as error:
        logging.error(f"Failed to connect to MQTT broker: {error}")
        return
    except OSError as error:
        logging.error(f"Network error while connecting to MQTT broker: {error}")
        return
    client.loop_start()

    try:
        while True:
            try:
                sensor_data = create_sensor_data()
                payload = json.dumps(sensor_data)
            except (TypeError, ValueError) as error:
                logging.error(f"Failed to create JSON payload: {error}")
                time.sleep(PUBLISH_INTERVAL_SECONDS)
                continue

            try:
                result = client.publish(TOPIC, payload)
            except RuntimeError as error:
                logging.error(f"Runtime error while publishing message: {error}")
                time.sleep(PUBLISH_INTERVAL_SECONDS)
                continue

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"Published message: {payload}")
            else:
                logging.warning(f"Failed to publish message. result_code={result.rc}")

            time.sleep(PUBLISH_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logging.info("Publisher stopped by user.")

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
