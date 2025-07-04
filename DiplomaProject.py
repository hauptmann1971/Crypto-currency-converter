# Программа "Конвертер криптовалют" для определения курса криптовалют к основным валютам

from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from datetime import datetime
import requests
import json
from config import *
#import psycopg2


# Загрузка словаря криптовалют через API
def setup_cryptocurrencies() -> None:
    global response
    try:
        url: str = URL_COINS
        headers: dict = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        response_json: list = list(json.loads(response.text))
        crypto: list = []
        for x in response_json:
            ls: tuple = (x['id'], x['name'])
            crypto.append(ls)
        crypto_currencies.update(dict(crypto))
    except Exception:
        mb.showerror("Ошибка при загрузке списка актуальных криптовалют", f"Возникла ошибка: {response.status_code}")


# Получение id выбранной криптовалюты из Combobox
def get_crypto(event: Event) -> None:
    global crypto_id
    crypto_name: str = combo_crypto.get()
    for k, v in crypto_currencies.items():
        if v == crypto_name:
            crypto_id = k


# Получение кода выбранной валюты из Combobox
def get_currency(event: Event) -> None:
    global currency_name
    currency_name = combo_currency.get()


# Получение кода валюты по ее имени
def get_currency_code() -> str:
    for k, v in currencies.items():
        if v == currency_name:
            return k


# Получение json-словаря о курсе криптовалюты к валюте
def get_rate() -> dict:
    global response
    url: str = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={get_currency_code()}"
    response = requests.get(url)
    return json.loads(response.text)


# Извлечение данных о курсе криптовалюты к валюте из словаря и отбражение информации в метке
def show_rate() -> None:
    global response
    try:
        response = get_rate()
        crypto: str = ''
        currency: str = ''
        rate: str = ''
        for k, v in response.items():
            crypto = k
            if v == {}:
                mb.showerror("Ошибка!", "По этой криптовалюте нет информации о курсе")
                lbl.config(text="")
                return
            for i, j in v.items():
                currency = i
                rate = j
        lbl.config(text=f'Курс "{crypto.upper()}" к\n"{currencies[currency.upper()]}": {rate: .6f}')
        now: datetime = datetime.now()
        lbl_date.config(text=f"Дата: {now.day}.{now.month}.{now.year}  Время: {now.hour} : {now.minute}")
        logger(rate, now)
    except Exception as exc:
        mb.showerror("Ошибка", f"Возникла ошибка:{response} / {exc}")
        lbl.config(text="")


# Инициализация базы данных Postgres для записи текущего курса криптовалюты к фиатной валюте и текущей даты и времени
def bd_init() -> None:
    try:
        conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST_IP)
        cursor = conn.cursor()
        with cursor as curs:    # создание таблицы crypto
            command = """CREATE TABLE crypto_currency
                                (ID INT PRIMARY KEY NOT NULL,
                                CRIPTO_NAME TEXT NOT NULL,
                                CURRENCY_NAME TEXT NOT NULL, 
                                RATE REAL NOT NULL,
                                TIME_POINT TIMESTAMP)"""
            curs.execute(command)
            conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


# Запись в базу данных
def logger(rate: str, now: datetime) -> None:
    try:
        conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST_IP)
        cursor = conn.cursor()
        with cursor as curs:
            command = "SELECT * FROM crypto_currency" #считывание строк из таблицы crypto
            curs.execute(command)
            print(curs.fetchall())
            if len(curs.fetchall()):
                id_last = curs.fetchall()[-1][0]
            else:
                id_last = 0
            command = """ INSERT INTO crypto_currency (ID, CRIPTO_NAME, CURRENCY_NAME, RATE, TIME_POINT)
                                       VALUES (%s,%s,%s,%s,%s)"""
            record = (id_last + 1, str(crypto_id), str(currency_name), rate, now)
            curs.execute(command, record)
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL:")
        print(error)



# Словарь основных криптовалют
crypto_currencies: dict = CRYPTO_CURRENCIES

# Словарь основных валют
currencies: dict = CURRENCIES

# Глобальные переменные для формирования запросов к API
crypto_id = DEFAULT_CRYPTO
currency_name = DEFAULT_CURRENCY_NAME
response = None

# Вызов функции для обновления словаря актуальных криптовалют
setup_cryptocurrencies()  # setup_cryptocurrencies()

# Графический интерфейс с основным циклом программы
root = Tk()
root.title(MAIN_WINDOW_TITLE)
icon = PhotoImage(file=MAIN_WINDOW_TITLE_ICON)
root.iconphoto(False, icon)
root.geometry(MAIN_WINDOW_GEOMETRY)

combo_crypto_var = StringVar(value=DEFAULT_CRYPTO)
lbl_crypto = ttk.Label(text=CRYPTO_CURRENCY_LABEL_TEXT, font=DEFAULT_FONT)
lbl_crypto.pack(pady=10)
combo_crypto = ttk.Combobox(root, textvariable=combo_crypto_var, values=list(crypto_currencies.values()),
                            font=DEFAULT_FONT)

combo_crypto.pack(pady=10)
combo_crypto.bind("<<ComboboxSelected>>", get_crypto)

combo_currency_var = StringVar(value=DEFAULT_CURRENCY_NAME)
lbl_currency = ttk.Label(text=CURRENCY_LABEL_TEXT, font=DEFAULT_FONT)
lbl_currency.pack(pady=10)
combo_currency = ttk.Combobox(root, textvariable=combo_currency_var, values=list(currencies.values()),
                              font=DEFAULT_FONT)
combo_currency.pack(pady=10)
combo_currency.bind("<<ComboboxSelected>>", get_currency)

lbl = ttk.Label(root, font=DEFAULT_FONT)
lbl.pack(pady=10)

btn = Button(root, text=BUTTON_TEXT, font=DEFAULT_FONT, command=show_rate)
btn.pack(pady=10, anchor="s")

lbl_date = ttk.Label(root, font=DEFAULT_FONT)
lbl_date.pack(pady=10)

#bd_init()

root.mainloop()
