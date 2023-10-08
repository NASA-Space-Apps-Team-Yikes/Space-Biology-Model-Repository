import csv
import psycopg2


# Function to establish a connection to the PostgreSQL database
def connect():
    # Attempting to establish a connection to the RDS PostgreSQL database
    try:
        conn = psycopg2.connect(host="model-zoo-space-apps.cqxs7dfl7szm.us-east-2.rds.amazonaws.com",
                                port="5432",
                                database="postgres",
                                user="***",
                                password="***")
        cursor = conn.cursor()
        print("Connected")
    except Exception as e:
        print("Connection failed: {}".format(e))  # Returns failure code
        return None, None  # If there's a failure, return None values

    return conn, cursor

def does_ensembl_id_exist(cursor, ensembl_id):
    cursor.execute("SELECT COUNT(*) FROM main_data WHERE ensembl_id = %s", (ensembl_id,))
    count = cursor.fetchone()[0]
    return count > 0  # returns True if count > 0, otherwise returns False

def insert_c3h_hej_data_from_csv(filename, cursor):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        print("C3H_HEJ DATA STARTED")
        for row in reader:
            ensembl_id = row['ensmbl_id']
            if not does_ensembl_id_exist(cursor, ensembl_id):
                print(f"Skipping row for ensembl_id {ensembl_id}: Not found in main_data")
                continue
            # Rename the columns as per the database table
            cleaned_row = {
                'ensembl_id': row['ensmbl_id'],
                'bsl_0days_avg': row['c3h_hej_bsl_0days_avg'],
                'flt_25days_avg': row['c3h_hej_flt_25days_avg'],
                'flt_75days_avg': row['c3h_hej_flt_75days_avg'],
                'gc_25days_avg': row['c3h_hej_gc_25days_avg'],
                'gc_75days_avg': row['c3h_hej_gc_75days_avg'],
                'viv_25days_avg': row['c3h_hej_viv_25days_avg'],
                'viv_75days_avg': row['c3h_hej_viv_75days_avg']
            }

            columns = ', '.join(cleaned_row.keys())
            placeholders = ', '.join(['%s'] * len(cleaned_row))
            sql = f"INSERT INTO c3h_hej_data ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(sql, list(cleaned_row.values()))
                print("Inserted row for ensembl_id:", row['ensmbl_id'])
            except Exception as e:
                print(f"Error inserting row for ensembl_id {row['ensmbl_id']}:", e)


def insert_c57_6j_data_from_csv(filename, cursor):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        print("C57_6J DATA STARTED")
        for row in reader:
            ensembl_id = row['ensmbl_id']
            if not does_ensembl_id_exist(cursor, ensembl_id):
                print(f"Skipping row for ensembl_id {ensembl_id}: Not found in main_data")
                continue
            cleaned_row = {
                'ensembl_id': row['ensmbl_id'],
                'bsl_0days_avg': row['c57_6j_bsl_0days_avg'],
                'flt_25days_avg': row['c57_6j_flt_25days_avg'],
                'flt_75days_avg': row['c57_6j_flt_75days_avg'],
                'gc_25days_avg': row['c57_6j_gc_25days_avg'],
                'gc_75days_avg': row['c57_6j_gc_75days_avg'],
                'viv_25days_avg': row['c57_6j_viv_25days_avg'],
                'viv_75days_avg': row['c57_6j_viv_75days_avg']
            }

            columns = ', '.join(cleaned_row.keys())
            placeholders = ', '.join(['%s'] * len(cleaned_row))
            sql = f"INSERT INTO c57_6j_data ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(sql, list(cleaned_row.values()))
                print("Inserted row for ensembl_id:", row['ensmbl_id'])
            except Exception as e:
                print(f"Error inserting row for ensembl_id {row['ensmbl_id']}:", e)


conn, cursor = connect()

if conn and cursor:
    # Inserts data from the corresponding CSV files. make sure to change the name of the CSV files
    # to match your file names 
    insert_c3h_hej_data_from_csv('processed_data_c3h.csv', cursor)
    insert_c57_6j_data_from_csv('processed_data_c57.csv', cursor)
    conn.commit()  # Commit the changes
    cursor.close()
    conn.close()