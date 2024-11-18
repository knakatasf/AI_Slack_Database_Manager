import mysql.connector
from mysql.connector import Error
import os
import sqlalchemy


from dotenv import load_dotenv

def connect():
    load_dotenv()
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("MYSQL_USER").strip(),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        if connection.is_connected():
            print("Connected to MySQL database using caching_sha2_password")
    except Error as e:
        print("Error while connecting to MySQL", e)

def add_client(client):
    pass
