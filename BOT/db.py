import sqlite3
import datetime

a_time1 = datetime.datetime.now()
a_time = str(a_time1).split('.')[0]  # <-- При помощи этой конструкции записываем время в формате 2023-07-06 19:36:39

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def create_user(us: int, name: str):  # <-- Функция которая проверяет есть ли в базе данных такой пользователь, если нет добавляет его.
	cursor.execute(f"SELECT telegram_id FROM user WHERE telegram_id = {us}")
	result = cursor.fetchone()

	if result is None:
		cursor.execute("INSERT INTO user (telegram_id, user_name, time_in) VALUES (?, ?, ?)", (us, name, a_time))
		conn.commit()


def create_pending_requests(us: int, text: str):  # <-- Функция которая записывает то что написал пользователь если
	cursor.execute(f"SELECT id FROM user WHERE telegram_id = {us}")  # это не нашлось в облаке.
	result = cursor.fetchone()
	text1 = str(text)
	cursor.execute("INSERT INTO pending_requests (text, time_in, user) VALUES (?, ?, ?)", (text1, a_time, result[0]))
	conn.commit()


def create_processed_requests(us: int, name: str, cat: str, text: str):  # <-- Функция которая записывает
	cursor.execute(f"SELECT telegram_id FROM user WHERE telegram_id = {us}")  # то что написал пользователь если программа
	result = cursor.fetchone()                                                # распознала его запрос
	if result is None:
		cursor.execute("INSERT INTO user (telegram_id, user_name, time_in) VALUES (?, ?, ?)", (us, name, a_time))
		conn.commit()

	cursor.execute(f"SELECT id FROM user WHERE telegram_id = {us}")
	user_id = cursor.fetchone()

	cursor.execute(f"SELECT id FROM categoryes WHERE category = '{cat}'")
	result2 = cursor.fetchone()

	text1 = str(text)
	cursor.execute("INSERT INTO processed_requests (text, time_in, category, user) VALUES (?, ?, ?, ?)", (text1, a_time, result2[0], user_id[0]))
	conn.commit()

def similar_request(text):  # <-- Функция которая возвращает какое было количество подобных запросов.
	text1 = str(text)
	cursor.execute(f'SELECT text, user, COUNT(*) FROM processed_requests  WHERE text = "{text1}" GROUP BY text, user')
	result = cursor.fetchall()
	user = 0
	zap = 0
	for i in result:
		user += 1
		zap += int(i[2])
	result2 = (user, zap)

	return result2
