import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from datetime import datetime
import json

mqttBroker = "broker.hivemq.com"

client = mqtt.Client("Machine1")
client.connect(mqttBroker)

dataObj = {}

while True:
    T = uniform(10.0, 50.0)
    T = round(T, 2)
    Terror = round(uniform(-3, 3), 2)
    P = randrange(50, 100)
    Perror = round(uniform(-10, 10), 2)
    H = randrange(10, 100)
    Herror = round(uniform(-2, 2), 2)

    now = datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + (now.second)
    date = datetime.now().date()

    dataObj["date"] = str(date)
    dataObj["seconds"] = total_time
    dataObj["Temperature"] = (T, Terror)
    dataObj["Pressure"] = (P, Perror)
    dataObj["Humidity"] = (H, Herror)

    jsondata = json.dumps(dataObj)
    client.publish("Pavel/Machine1/SensorData", jsondata, qos=0)

    print("Data published..,", dataObj)

    time.sleep(1.0)