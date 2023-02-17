import paho.mqtt.client as mqtt
import time
import json
import psycopg2 as pg

# conn = pg.connect("dbname=DashboardDB user='postgres' host='localhost' password='7323'")

# try:
#     cur = conn.cursor()
#     print("Connection established")
# except (Exception, pg.DatabaseError) as error:
#     print(error)


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

    insertQ = """ INSERT INTO manufacturing."sensorData" ("machine_id", "timestamp", "date", "pressure", "temperature", "humidity")
                        VALUES(%s,%s,%s,%s,%s,%s)"""
    record = (machine_id, timestamp, date, pressure, temperature, humidity)

    # try:
    #     cur.execute(insertQ, record)
    #     print("DB Transaction executed")
    #
    #     # commit all transactions after the loop has stopped.
    #     conn.commit()
    #
    # except (Exception, pg.DatabaseError) as error:
    #     print(error)



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
print("All DB Transactions committed")