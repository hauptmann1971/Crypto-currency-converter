from config import *
from db_init import db_init
import  mysql.connector
import datetime

def is_committed(cursor, lst: list) -> bool:
    command = f"USE {DATABASE_NAME}; SELECT COUNT(*) FROM crypto_currency;"
    lst_committed = cursor.execute(command, multi = True)
    if set(lst) == set(lst_committed):
        return True
    else:
        return False
                  



def logger(lst: list) -> str:
    db_init()
    command = f"""
    USE {DATABASE_NAME};
    INSERT crypto_currency(crypto_name, currency_name, rate, time_point)
    VALUES('{lst[0]}', '{lst[1]}', {lst[2]}, '{datetime.datetime.now().strftime("%y-%m-%d %I:%M:%S")}');"""
    print(command)
    try:
        connection = mysql.connector.connect(host=HOST_IP,
                                             user=USER_NAME,
                                             password=PASSWORD)
        cursor = connection.cursor()
        cursor.execute(command, multi=True)
        connection.commit()
        if is_committed(cursor, lst):
            cursor.close()
            connection.close()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()

logger(lst = ['bitcoin', 'EUR', 22222.0])
