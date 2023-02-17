import psycopg2 as pg
import csv

conn = pg.connect("host=localhost dbname=DashboardDB user=postgres password='7323'")
cur = conn.cursor()


def createTable():
    insertCMD = '''
                CREATE TABLE public."machines"(
                    id integer PRIMARY KEY,
                    name text,
                    type text,
                    vendor text
                )
                '''
    cur.execute(insertCMD)

def insertRow():
    insertCMD = """INSERT INTO public."machines" VALUES (%s, %s, %s, %s) """
    values = (10, "HAAS VF2", "CNC Turning", "ABC Corp")
    cur.execute(insertCMD, values)


def bulkInsert():
    with open ('machinedata.csv', 'r') as content:
        next(content)
        cur.copy_from(content, 'public."machines"', sep=',')


#createTable()
#insertRow()
bulkInsert()
conn.commit()