import time

from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import pandas as pd
import os

import paho.mqtt.client as mqtt
from sub_JSON import *

conn = pg.connect(os.environ.get("DATABASE_URL"), sslmode="require")

try:
    cur = conn.cursor()
    print("App connection established")
except (Exception, pg.DatabaseError) as error:
    print(error)

app = Flask(__name__)
api = Api(app)


# MAIN MQTT Initializations
mqttBroker = "broker.hivemq.com"

client = mqtt.Client("PC 1")
client.connect(mqttBroker)

# call-back functions
client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message
client.on_disconnect = on_disconnect


class Welcome(Resource):
    def get(self):
        return jsonify({"Welcome to the REST server": "Type '.../all' for more commands"})

class All(Resource):
    def get(self):
        uriObj = {}

        uriObj["list of resources"] = ".../all"
        uriObj["Machine List"] = ".../machinelist"
        uriObj["Add a Machine"] = ".../add"
        uriObj["Retrieve Sensor Data"] = ".../retrieve?start='start'&end='end'"
        uriObj["Last 200 records"] = ".../last200"
        uriObj["Start recording to DB"] = ".../startmqtt"
        uriObj["Stop recording to DB"] = ".../stopmqtt"

        return jsonify(uriObj)


class Machines(Resource):
    def get(self):
        try:
            qCmd = 'SELECT * FROM public."machine_asset"'
            cur.execute(qCmd)
            records = cur.fetchall()

            return jsonify({'machineList': [rec for rec in records]})

        except (Exception, pg.DatabaseError) as error:
            print(error)

    def post(self):
        m_id = request.args.get("machine_id")
        m_name = request.args.get("mach_name")

        try:
            insert_query = """ INSERT INTO public."machine_asset" ("machine_id", "machine_name") VALUES( %s, %s) """
            record = (m_id, m_name)
            cur.execute(insert_query, record)
            conn.commit()

            return jsonify({'msg': "Record is added"})

        except (Exception, pg.DatabaseError) as error:
            return jsonify({'msg': "Something went wrong..wrong entry"})


class MachineData(Resource):
    def get(self):
        start = request.args.get("start")
        end = request.args.get("end")

        try:
            qCmd = f'SELECT * FROM public."sensorData" WHERE timestamp > {start} AND timestamp <= {end} ORDER BY timestamp DESC LIMIT 200;'
            df = pd.read_sql_query(qCmd, conn)

            if df.empty:
                qCmd = f'SELECT * FROM public."sensorData" ORDER BY timestamp DESC LIMIT 200'
                df = pd.read_sql_query(qCmd, conn)

            df['temperature'] = df['temperature'].apply(lambda x: x[0])
            df['pressure'] = df['pressure'].apply(lambda x: x[0])
            df['humidity'] = df['humidity'].apply(lambda x: x[0])

            return df.to_json()

        except (Exception, pg.DatabaseError) as error:
            return 204, jsonify({'msg': "Something went wrong..wrong entry"})


class MachineDataLast(Resource):
    def get(self):
        try:
            qCmd = 'SELECT * FROM public."sensorData" ORDER by timestamp DESC LIMIT 200'
            df = pd.read_sql_query(qCmd, conn)

            df['temperature'] = df['temperature'].apply(lambda x: x[0])
            df['pressure'] = df['pressure'].apply(lambda x: x[0])
            df['humidity'] = df['humidity'].apply(lambda x: x[0])

            return df.to_json()

        except (Exception, pg.DatabaseError) as error:
            print(error)
            return jsonify({'msg': "Something went wrong..wrong entry"})

class Mqttstart(Resource):
    def get(self):
        client.connect(mqttBroker)
        print("MQTT subscribe started")
        client.subscribe("Pavel/Machine1/SensorData")
        # client.loop_forever()
        client.loop_start()
        time.sleep(3)
        client.loop_stop()
        print("MQTT subscribe stopped")
        return jsonify({"Status": "MQTT LOOP STOPPED"})

class Mqttstop(Resource):
    def get(self):
        client.disconnect()
        return jsonify({"Status": "MQTT Subscribe Disconnected"})

api.add_resource(Welcome, '/')
api.add_resource(All,'/all')
api.add_resource(Machines, '/machinelist', '/add')
api.add_resource(MachineData,'/retrieve')
api.add_resource(MachineDataLast,'/last200')
api.add_resource(Mqttstart, '/startmqtt')
api.add_resource(Mqttstop, '/stopmqtt')

if __name__ == '__main__':
    app.run(port='3000', debug=True)
