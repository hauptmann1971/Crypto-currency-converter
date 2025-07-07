import mysql.connector
from mysql.connector import Error
from datetime import datetime
from config import *

# Конфигурация подключения к БД
DB_CONFIG = {
    'host': HOST_IP,
    'port': DB_PORT,
    'user': USER_NAME,
    'password': PASSWORD,
    'database': DATABASE_NAME
}


def create_table() -> None:
    """Создает таблицу crypto_currency, если она не существует"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        record = """
        CREATE TABLE IF NOT EXISTS crypto_currency (
            id INT AUTO_INCREMENT PRIMARY KEY,
            crypto_name VARCHAR(50) NOT NULL,
            currency_name VARCHAR(10) NOT NULL,
            exchange_rate DECIMAL(20, 8) NOT NULL,
            timestamp DATETIME NOT NULL,
            INDEX (crypto_name, currency_name));
        """
        cursor.execute(record)
        conn.commit()
        print("Таблица crypto_currency успешно создана или уже существовала")

    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def insert_data(crypto_name: str, currency_name: str, exchange_rate: float) -> bool:
    """Вставляет данные о курсе криптовалюты в БД"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO crypto_currency (crypto_name, currency_name, exchange_rate, timestamp)
        VALUES (%s, %s, %s, %s)
        """
        current_time = datetime.now()
        record = (crypto_name, currency_name, exchange_rate, current_time)

        cursor.execute(insert_query, record)
        conn.commit()
        record = f'''SELECT * FROM crypto_currency
                     WHERE ID = {cursor.lastrowid};'''
        cursor.execute(record)
        last_record = cursor.fetchone()
        print(last_record[1::])
        print([currency_name, currency_name, exchange_rate, current_time])
        if last_record[1::] == [currency_name, currency_name, exchange_rate, current_time]:
            return True
        else:
            return False

    except Error as e:
        print(f"Ошибка при вставке данных: {e}")
        conn.rollback()
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

