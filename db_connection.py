import mysql.connector

db_conn = None


def get_db_connection():
    global db_conn
    if not db_conn:
        db_conn = mysql.connector.connect(
            host='remotemysql.com',
            port=3306,
            user='6u0Lxq4dME',
            password='fKZFAGvLAY',
            database='6u0Lxq4dME'
        )

    return db_conn
