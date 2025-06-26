import mysql.connector
from tkinter import messagebox as mb

from config import DATABASE_NAME, USER_NAME, PASSWORD, HOST_IP


def db_init() -> None:
    try:
        with mysql.connector.connect(database=DATABASE_NAME,
                                     user=USER_NAME,
                                     password=PASSWORD,
                                     host=HOST_IP) as conn:
            command = f"""CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}
                                   USE {DATABASE_NAME}"""
            with conn.cursor() as cursor:
                cursor.execute(command)
                conn.commit()
    except mysql.connector.Error as e:
        mb.showerror("Ошибка!", str(e))

db_init()
        

