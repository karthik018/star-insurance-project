import mysql.connector
import os

db_conn = None


def get_db_connection():
    global db_conn
    if not db_conn:
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DATABASE')
        db_conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

    return db_conn
