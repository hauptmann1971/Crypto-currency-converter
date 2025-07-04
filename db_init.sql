CREATE DATABASE IF NOT EXISTS mysql_database;
CREATE TABLE IF NOT EXISTS mysql_table (ID INT PRIMARY KEY NOT NULL,
                                        CRIPTO_NAME TEXT NOT NULL,
                                        CURRENCY_NAME TEXT NOT NULL,
                                        RATE REAL NOT NULL,
                                        TIME_POINT TIMESTAMP);