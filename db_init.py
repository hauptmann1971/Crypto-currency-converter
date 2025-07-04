import mysql.connector
from config import *

try:
    with mysql.connector.connect(host=HOST_IP,
                                 user=USER_NAME,
                                 password=PASSWORD) as connection:
        with connection.cursor() as cursor:
            print(cursor.execute("SELECT * FROM crypto_currency;"))
        print(connection.get_server_info())
except mysql.connector.Error as error:
    print(error)
