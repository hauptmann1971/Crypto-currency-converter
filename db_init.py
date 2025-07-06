import mysql.connector as mysqlconn
from config import *


def sql_query(query: str) -> str:
    lst = [i.split() for i in query.split(';')]
    print(lst)



content = ''
try:
    with open(SQL_FILE_NAME, 'r') as file:
        content = file.read()
        command = content
        print(content)
except FileNotFoundError as e:
        print(e)

with mysqlconn.connect(host=HOST_IP,
                       user=USER_NAME,
                       password=PASSWORD) as connection:
    try:
            with connection.cursor() as cursor:
                cursor.execute(command)

    except mysqlconn.Error as e:
        print(e)
