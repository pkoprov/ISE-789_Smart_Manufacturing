import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code: {}".format(rc))

def on_message(client, userdata, message):
    print("Received message:", message.topic)

    if message.topic == "Pavel/Machine1/SensorData/Temperature":
        msg = message.payload.decode("utf-8")
        date = msg.split("_")[0]
        seconds = msg.split("_")[1]
        temperature = msg.split("_")[2]
        print("T: ", temperature)

    if message.topic == "Pavel/Machine1/SensorData/Pressure":
        msg = message.payload.decode("utf-8")
        date = msg.split("_")[0]
        seconds = msg.split("_")[1]
        pressure = msg.split("_")[2]
        print("P: ", pressure)

    if message.topic == "Pavel/Machine1/SensorData/Humidity":
        msg = message.payload.decode("utf-8")
        date = msg.split("_")[0]
        seconds = msg.split("_")[1]
        humidity = msg.split("_")[2]
        print("H:", humidity)

def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)


mqttBroker = "broker.hivemq.com"

client = mqtt.Client("PC 1")
client.connect(mqttBroker)

client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.loop_start()

client.subscribe("Pavel/Machine1/SensorData/#")
time.sleep(5)

client.loop_stop()