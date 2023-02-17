import pandas as pd
import json
import requests

def sensorData(start, stop):

    resp = requests.get("https://pasha-rest-server.herokuapp.com/retrieve?start=" + str(start) + "&end=" + str(stop))

    if resp.status_code == 200:
        records = json.loads(resp.content)
        df = pd.read_json(records)

    if resp.status_code == 204:
        resp = requests.get("https://pasha-rest-server.herokuapp.com/last200")
        if resp.status_code == 200:
            records = json.loads(resp.content)
            df = pd.read_json(records)

    return df


def getsensorData200():
    resp = requests.get("https://binilrestserver.herokuapp.com/last200")
    if resp.status_code == 200:
        records = json.loads(resp.content)
        df = pd.read_json(records)

    return df
