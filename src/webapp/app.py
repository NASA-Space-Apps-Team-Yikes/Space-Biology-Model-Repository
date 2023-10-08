import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def connect_to_database():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(host=os.getenv("DB_HOST"),
                                port=os.getenv("DB_PORT"),
                                database=os.getenv("DB_NAME"),
                                user=os.getenv("DB_USER"),
                                password=os.getenv("DB_PASSWORD"))
        cursor = conn.cursor()
        print("Connected")
    except Exception as e:
        print("Connection failed: {}".format(e))
        print("Exception message: {}".format(e))
    return conn, cursor

@app.route('/database')
def database():
    conn, cursor = connect_to_database()
    if cursor is not None:
        try:
            cursor.execute("SELECT * FROM c57_6j_data WHERE ensembl_id = 'ENSMUSG00000000031'")
            rows = cursor.fetchall()
        except Exception as e:
            print("Failed to fetch data: {}".format(e))
            rows = []
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
        return str(rows)
    else:
        return "Failed to connect to the database"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)