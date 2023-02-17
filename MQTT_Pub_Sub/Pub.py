import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from datetime import datetime

mqttBroker = 'broker.hivemq.com'

client = mqtt.Client('Machine1')
client.connect(mqttBroker)

while True:
    T = round(uniform(10, 200), 2)
    T_error = round(uniform(-3,3),2)

    P = round(uniform(50,100),2)
    P_error = round(uniform(-5,5),2)

    H = randrange(10, 100)
    H_error = round(uniform(-2, 2), 2)

    now = datetime.now()
    date = datetime.now().date()
    total_time = now.hour*3600+now.minute*60+now.second

    Tmsg = str(date) + "_" + str(total_time) + "_" + str(T) + "_" + str(T_error)
    client.publish("Pavel/Machine1/SensorData/Temperature", Tmsg, qos=0)

    Pmsg = str(date) + "_" + str(total_time) + "_" + str(P) + "_" + str(P_error)
    client.publish("Pavel/Machine1/SensorData/Pressure", Pmsg, qos=0)

    Hmsg = str(date) + "_" + str(total_time) + "_" + str(H) + "_" + str(H_error)
    client.publish("Pavel/Machine1/SensorData/Humidity", Hmsg, qos=0)

    print("Just published Temperature " + Tmsg)
    print("Just published Pressure " + Pmsg)
    print("Just published Humidity " + Hmsg)

    time.sleep(1.0)

