# config.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Cambia si usas otra contraseña o puerto
DB_URI = "mysql+pymysql://admin:Admin123!@localhost/hamburguesas"





# # config.py

# import pymysql

# def get_connection():
#     return pymysql.connect(
#         host="localhost",
#         user="admin",
#         password="Admin123!",
#         database="hamburguesas",
#         cursorclass=pymysql.cursors.DictCursor
#     )
