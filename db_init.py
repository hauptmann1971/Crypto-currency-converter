import mysql.connector as mysqlconn
from config import *

def db_init() -> None:
    content = ''
    try:
        with open(SQL_FILE_NAME, 'r') as file:
            content = file.read()
            command = content
            #print(content)
    except FileNotFoundError as e:
            print(e)

    connection = mysqlconn.connect(host=HOST_IP,
                           user=USER_NAME,
                           password=PASSWORD)
    try:
        cursor = connection.cursor()
        cursor.execute(command)
    except mysqlconn.Error as e:
        print(e)


