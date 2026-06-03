# MQTT-Based IoT Sensor Monitoring System


## Overview

This project is a simple MQTT-based IoT sensor monitoring system built with Python.

It simulates IoT sensor data such as temperature and humidity, publishes the data to a Mosquitto MQTT broker, and receives the data with a subscriber application. The subscriber parses JSON messages, validates the received data, and logs both normal and abnormal events.

The purpose of this project is to demonstrate basic MQTT communication, JSON data handling, error handling, and logging in an IoT-style system.


## Features

- Simulates IoT sensor data using Python
- Publishes sensor data to a Mosquitto MQTT broker
- Subscribes to an MQTT topic and receives sensor data
- Uses JSON as the message format
- Parses and validates received JSON messages
- Handles invalid JSON, missing fields, and invalid data types
- Logs events to both console and log files
- Detects normal and unexpected MQTT disconnections


## System Architecture

```text
[Publisher]
    |
    | MQTT publish
    | Topic: iot/sensor/temperature
    v
[Mosquitto MQTT Broker]
    |
    | MQTT subscribe
    v
[Subscriber]
    |
    | Decode payload
    | Parse JSON
    | Validate data
    v
[Console / Log Files]
```


## Technologies Used

- Python 3
- paho-mqtt
- Mosquitto MQTT Broker
- JSON
- Python logging module


## Project Structure

```text
mqtt-iot-monitor/
├── publisher.py
├── subscriber.py
├── requirements.txt
├── README.md
├── .gitignore
└── logs/
    ├── publisher.log
    └── subscriber.log
```

The `logs/` directory is created automatically at runtime and is not tracked by Git.


## Requirements

- Python 3.10 or later
- Mosquitto
- paho-mqtt


## How to Run

Coming soon.


## Example Output

Publisher output:
2026-06-02 10:00:01 [INFO] Connected to MQTT broker.
2026-06-02 10:00:04 [INFO] Published message: {"device_id": "sensor-001", "temperature": 24.5, "humidity": 58, "timestamp": "2026-06-02T10:00:04"}

Subscriber output:
2026-06-02 10:00:04 [INFO] Connected to MQTT broker.
2026-06-02 10:00:04 [INFO] Subscribed to topic: iot/sensor/temperature
2026-06-02 10:00:04 [INFO] Received data from sensor-001: temperature=24.5, humidity=58, timestamp=2026-06-02T10:00:04


## Error Handling

The subscriber handles several types of invalid input:
- Invalid UTF-8 payload
- Invalid JSON format
- JSON data that is not an object
- Missing required fields
- Invalid data types


## Test Cases

The following cases were tested:

| Case | Expected Result |
|---|---|
| Valid sensor data | Subscriber receives and logs the data |
| Invalid JSON message | Subscriber logs a warning and continues running |
| JSON array instead of object | Subscriber logs an invalid data format warning |
| Missing required field | Subscriber logs a missing key warning |
| Invalid data type | Subscriber logs an invalid data type warning |
| Publisher stopped with Ctrl + C | Publisher disconnects gracefully |
| Broker stopped unexpectedly | Publisher and subscriber detect unexpected disconnection |


## Future Improvements MQTT Connectivity Validator

- Add automatic reconnection handling
- Support multiple sensor devices
- Store received data in CSV or a database
- Add MQTT authentication
- Add TLS support using port 8883
- Add Docker support for the MQTT broker and applications
- Add unit tests for data validation logic


