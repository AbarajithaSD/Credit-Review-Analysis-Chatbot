#step15
import mysql.connector
from mysql.connector import Error

from config import Config


def get_connection():

    try:

        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )

        return connection

    except Error as error:

        print(
            f"MySQL connection error: {error}"
        )

        raise