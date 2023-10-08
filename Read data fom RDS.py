
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

def read_data_from_table(cursor, table_name):
    """Read and display the first 5 columns for a given table."""

    # Execute the query
    cursor.execute(f"SELECT * FROM {table_name};")  # Limit to 5 rows for demonstration

    # Fetch column names (will fetch first 5)
    colnames = [desc[0] for desc in cursor.description]

    # Fetch rows
    rows = cursor.fetchall()

    # Display the data
    for row in rows:
        for idx, col_name in enumerate(colnames):
            print(f"{col_name}: {row[idx]}")
        print("------")  # Separator for clarity

def fetch_all_ensembl_ids(cursor, table_name):
    """Fetch and return all ensembl_id values from a specified table."""
    cursor.execute(f"SELECT ensembl_id FROM {table_name};")
    return [row[0] for row in cursor.fetchall()]

conn, cursor = connect()
if conn and cursor:
    print("Data from c3h_hej_data:")
    read_data_from_table(cursor, 'c3h_hej_data')
    print("\nData from c57_6j_data:")
    read_data_from_table(cursor, 'c57_6j_data')
    cursor.close()
    conn.close()