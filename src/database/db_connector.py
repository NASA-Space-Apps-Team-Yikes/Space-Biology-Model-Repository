import psycopg2

def connect():
    try:
        conn = psycopg2.connect(host="model-zoo-space-apps.cqxs7dfl7szm.us-east-2.rds.amazonaws.com",
                                port="5432",
                                database="postgres",
                                user="postgress_space",
                                password="SpaceApps2023!")
        cursor = conn.cursor()
        print("Connected")

    except Exception as e:
        print("Connection failed: {}".format(e))
    return conn, cursor

connect()