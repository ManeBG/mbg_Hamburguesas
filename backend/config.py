# config.py

import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="admin",
        password="Admin123!",
        database="hamburguesas",
        cursorclass=pymysql.cursors.DictCursor
    )
