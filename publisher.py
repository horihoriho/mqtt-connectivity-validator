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

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            sensor_data = create_sensor_data()
            payload = json.dumps(sensor_data)

            result = client.publish(TOPIC, payload)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.info(f"Published: {payload}")
            else:
                logging.warning(f"Failed to publish message. result_code={result.rc}")

            time.sleep(3)

    except KeyboardInterrupt:
        logging.info("\nPublisher stopped by user.")

    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
