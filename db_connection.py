import mysql.connector

db_conn = None


def get_db_connection():
    global db_conn
    if not db_conn:
        db_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='StarProject'
        )

    return db_conn
