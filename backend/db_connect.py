import mysql.connector


def database_connect():
    mysql_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="travel_app"
    )

    return mysql_db

