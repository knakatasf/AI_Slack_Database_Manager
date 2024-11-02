# import mysql.connector




# def connect():
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="slackbot_user",  # Use the MySQL username you set in Docker
#         password="slackbot_password",  # Use the password you set
#         database="slackbot_db"  # Name of the database
#     )
#     cursor = connection.cursor()
#     cursor.execute("SELECT DATABASE()")
#     db_name = cursor.fetchone()
#     print("Connected to database:", db_name)


import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
import os

def connect():
    load_dotenv()


    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your host, e.g., '127.0.0.1' or a Docker container name
            user=os.getenv("MYSQL_USER").strip(),  # Replace with your MySQL username
            password= os.getenv("MYSQL_PASSWORD").strip(),  # Replace with your MySQL password
            database=os.getenv("MYSQL_DB").strip()  # Replace with the name of your database
        )

        if connection.is_connected():
            print("Connected to MySQL database using caching_sha2_password")

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

