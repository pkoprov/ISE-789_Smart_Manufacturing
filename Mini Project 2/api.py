import pandas as pd
import psycopg2 as pg


try:
    conn = pg.connect(
            "postgres://nbsxtkkvgvgjtl:76c69fc2d1b3c6e77a7168363718f817556d1468e5214a10a78c9e1b733067a0@ec2-54-237-143-127.compute-1.amazonaws.com:5432/d7jo057msb165k", sslmode='require')
    curr = conn.cursor()
    print('Connection established')
except (Exception, pg.DatabaseError) as error:
    print(error)


def sensorData(start, stop):

    qCmd = f'SELECT * FROM public."sensorData" WHERE timestamp > {start} AND timestamp <= {stop};'
    df = pd.read_sql_query(qCmd, conn)

    if df.empty:
        qCmd = f'SELECT * FROM public."sensorData" ORDER BY timestamp DESC LIMIT 100;'
        df = pd.read_sql_query(qCmd, conn)
        date = df["date"].head(1)[0]
        hrs = df["timestamp"].head(1)[0]//3600
        mnts = (df["timestamp"].head(1)[0]-hrs*3600)//60
        sec = df["timestamp"].head(1)[0] - hrs*3600 - mnts*60
        msg = f'Subscriber is off. Last record was published on {date} at {hrs}:{mnts}:{sec}'

    df['temperature'] = df['temperature'].apply(lambda x: x[0])
    df['pressure'] = df['pressure'].apply(lambda x: x[0])
    df['humidity'] = df['humidity'].apply(lambda x: x[0])

    return df
