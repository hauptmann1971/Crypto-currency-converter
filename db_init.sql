USE kalmyk3j_romanov;
CREATE TABLE IF NOT EXISTS crypto_currency(id int AUTO_INCREMENT PRIMARY KEY,
										   crypto_name text not null,
										   currency_name text not null,
										   rate double not null,
										   time_point timestamp not null);