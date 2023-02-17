import paho.mqtt.client as mqtt
import time
import json
import psycopg2 as pg

conn = pg.connect(
            "postgres://nbsxtkkvgvgjtl:76c69fc2d1b3c6e77a7168363718f817556d1468e5214a10a78c9e1b733067a0@ec2-54-237-143-127.compute-1.amazonaws.com:5432/d7jo057msb165k", sslmode='require')

try:
    cur = conn.cursor()
    print("Connection established")
except (Exception, pg.DatabaseError) as error:
    print(error)


def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code: {}".format(rc))

def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)

def on_message(client, userdata, message):
    print("Received message:", message.topic)
    msg = message.payload.decode("utf-8")
    dataObj=json.loads(msg)

    machine_id = 1002
    date = dataObj["date"]
    timestamp = dataObj["seconds"]
    temperature = dataObj["Temperature"]
    pressure = dataObj["Pressure"]
    humidity = dataObj["Humidity"]

    insertQ = """ INSERT INTO public."sensorData" ("machine_id", "timestamp", "date", "pressure", "temperature", "humidity")
                        VALUES(%s,%s,%s,%s,%s,%s)"""
    record = (machine_id, timestamp, date, pressure, temperature, humidity)

    try:
        cur.execute(insertQ, record)
        print("DB Transaction executed")

        # commit all transactions after the loop has stopped.
        conn.commit()
        print("All DB Transactions committed")
    except (Exception, pg.DatabaseError) as error:
        print(error)



#MAIN
mqttBroker = "broker.hivemq.com"

client = mqtt.Client("PC 1")
client.connect(mqttBroker)

#call-back functions
client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message


client.loop_start()

client.subscribe("Pavel/PashaRPI/SensorData")
time.sleep(10)

client.loop_stop()
