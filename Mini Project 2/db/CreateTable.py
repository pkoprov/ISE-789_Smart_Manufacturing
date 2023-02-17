import psycopg2 as pg


def create_table():
    conn = None
    try:
        # connecting to Heroku postgres DB
        conn = pg.connect(
            "postgres://nbsxtkkvgvgjtl:76c69fc2d1b3c6e77a7168363718f817556d1468e5214a10a78c9e1b733067a0@ec2-54-237-143-127.compute-1.amazonaws.com:5432/d7jo057msb165k", sslmode='require')
        cur = conn.cursor()
        print("Connection established")

        # create a table within a cloud DB
        createCMD = """CREATE TABLE public."sensorData"
                    (
                        machine_id integer NOT NULL,
                        temperature double precision[],
                        pressure double precision[],
                        humidity double precision[],
                        "timestamp" integer,
                        date date NOT NULL,
                        CONSTRAINT "sensorData_pkey" PRIMARY KEY (machine_id, "timestamp", date)
                    )
                    
                    TABLESPACE pg_default;
                    
                    ALTER TABLE public."sensorData"
                        OWNER to nbsxtkkvgvgjtl;
                    """
        cur.execute(createCMD)

        cur.close()

        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    create_table()