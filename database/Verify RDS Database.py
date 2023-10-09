''' This Python program provides functionality to establish a connection with an
RDS PostgreSQL database. The `connect` function attempts to establish this connection
and returns the connection and cursor objects if successful. Upon connection, the
program confirms the successful connection by printing "Connected".
If the connection fails, it provides an error message detailing the failure. We are
modeling this database off of the OSD-253 NASA Study https://osdr.nasa.gov/bio/repo/data/studies/OSD-253
 '''

import psycopg2

def connect():
    # Attempting to establish a connection to the RDS PostgreSQL database
    try:
        conn = psycopg2.connect(host="model-zoo-space-apps.cqxs7dfl7szm.us-east-2.rds.amazonaws.com",
                                port="5432",
                                database="postgres",
                                user="postgress_space",
                                password="SpaceApps2023!")
        cursor = conn.cursor()
        print("Connected")
    except Exception as e:
        print("Connection failed: {}".format(e))  # Returns failure code
        return None, None  # If there's a failure, return None values

    return conn, cursor

def create_tables(conn, cursor):
    try:
        # Creating the main table that holds the unique ensembl_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS main_data (
                ensembl_id VARCHAR PRIMARY KEY
            )
        """)

        # Creating a table specific to data for the 'c3h-hej' mouse
        # This table references the main_data table through the ensembl_id field
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS c3h_hej_data (
                ensembl_id VARCHAR REFERENCES main_data(ensembl_id),
                bsl_0days_avg FLOAT,
                flt_25days_avg FLOAT,
                flt_75days_avg FLOAT,
                gc_25days_avg FLOAT,
                gc_75days_avg FLOAT,
                viv_25days_avg FLOAT,
                viv_75days_avg FLOAT,
                PRIMARY KEY (ensembl_id)
            )
        """)

        # Creating a table specific to data for the 'c57-6j' mouse
        # This table also references the main_data table through the ensembl_id field
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS c57_6j_data (
                ensembl_id VARCHAR REFERENCES main_data(ensembl_id),
                bsl_0days_avg FLOAT,
                flt_25days_avg FLOAT,
                flt_75days_avg FLOAT,
                gc_25days_avg FLOAT,
                gc_75days_avg FLOAT,
                viv_25days_avg FLOAT,
                viv_75days_avg FLOAT,
                PRIMARY KEY (ensembl_id)
            )
        """)

        # Committing the changes (i.e., creating the tables) to the database
        conn.commit()
        print("Tables created successfully")
    except Exception as e:
        print("Failed to create tables: {}".format(e))

# Connecting to the database
conn, cursor = connect()
# If the connection is successful, create the tables
if conn and cursor:
    create_tables(conn, cursor)
    # Close the cursor and connection after finishing
    cursor.close()
    conn.close()
