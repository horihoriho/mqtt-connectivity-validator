# -*- coding: utf-8 -*-

import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# Publisher settings
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/sensor/temperature"


def create_sensor_data():
    return {
        "device_id": "sensor-001",
        "temperature": round(random.uniform(20.0, 30.0), 1),
        "humidity": random.randint(40, 70),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    try:
        while True:
            sensor_data = create_sensor_data()
            payload = json.dumps(sensor_data)

            result = client.publish(TOPIC, payload)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published: {payload}")
            else:
                print(f"Failed to publish message. result_code={result.rc}")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nPublisher stopped by user.")

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
