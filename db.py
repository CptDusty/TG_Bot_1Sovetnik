import sqlite3
import datetime
from dateutil.relativedelta import relativedelta

def get_connection():
    return sqlite3.connect("database.db")

# Функции для работы с БД
def check_user(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_info = cursor.fetchone()
    cursor.close()
    connection.close()
    if user_info is not None:
        return True
    else: 
        return False

def get_users(user_id: int, spec_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users where user_id != ? and speciality = ? ORDER BY last_name", (user_id, spec_id,))
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def get_users_wspec(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users where user_id != ? ORDER BY last_name", (user_id,))
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def get_specialities():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialities ORDER BY (id = 12), name")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users
def get_specialities_for_reg(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialities WHERE id = ? ORDER BY (id = 12), Name",(id,))
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users
def get_speciality_name_for_reg(id:int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM specialities WHERE id = ?",(id))
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users
def get_specialities_id():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Id FROM specialities")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def get_user_info(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_info = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_info

def save_thanks(sender_id: int, receiver_id: int, text: str):
    connection = get_connection()
    cursor = connection.cursor()
    dt = datetime.datetime.now()
    dt2= dt.date()
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, text, date) VALUES (?, ?, ?, ?)",
                   (sender_id, receiver_id, text, dt2))
    connection.commit()
    cursor.close()
    connection.close()

def get_top_thanks_s():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT users.first_name, users.last_name, COUNT(messages.text) as message_count FROM messages INNER JOIN users ON messages.sender_id = users.user_id GROUP BY users.user_id ORDER BY message_count DESC LIMIT 10")
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_top_thanks_curr_s():
    connection = get_connection()
    cursor = connection.cursor()
    first_day_of_current_month = datetime.date.today().replace(day=1)
    cursor.execute("SELECT users.first_name, users.last_name, COUNT(messages.text) as message_count FROM messages INNER JOIN users ON messages.sender_id = users.user_id WHERE messages.date > ? GROUP BY users.user_id ORDER BY message_count DESC LIMIT 10", (first_day_of_current_month,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_top_thanks_prev_s():
    connection = get_connection()
    cursor = connection.cursor()
        # Получаем первый день прошлого месяца
    first_day_of_last_month = datetime.date.today().replace(day=1) - relativedelta(months=1)
    # Получаем последний день прошлого месяца
    last_day_of_last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    cursor.execute("SELECT users.first_name, users.last_name, COUNT(messages.text) as message_count FROM messages INNER JOIN users ON messages.sender_id = users.user_id WHERE messages.date > ? and messages.date <= ? GROUP BY users.user_id ORDER BY message_count DESC LIMIT 10", (first_day_of_last_month, last_day_of_last_month,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_top_thanks_r():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT users.first_name, users.last_name, COUNT(messages.text) as message_count FROM messages INNER JOIN users ON messages.receiver_id = users.user_id GROUP BY users.user_id ORDER BY message_count DESC LIMIT 10")
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_top_thanks_curr_r():
    connection = get_connection()
    cursor = connection.cursor()
    first_day_of_current_month = datetime.date.today().replace(day=1)
    cursor.execute("SELECT users.first_name, users.last_name, COUNT(messages.text) as message_count FROM messages INNER JOIN users ON messages.receiver_id = users.user_id WHERE messages.date > ? GROUP BY users.user_id ORDER BY message_count DESC LIMIT 10", (first_day_of_current_month,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_top_thanks_prev_r():
    connection = get_connection()
    cursor = connection.cursor()
        # Получаем первый день прошлого месяца
    first_day_of_last_month = datetime.date.today().replace(day=1) - relativedelta(months=1)
    # Получаем последний день прошлого месяца
    last_day_of_last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    cursor.execute("SELECT users.first_name, users.last_name, COUNT(messages.text) as message_count FROM messages INNER JOIN users ON messages.receiver_id = users.user_id WHERE messages.date > ? and messages.date <= ? GROUP BY users.user_id ORDER BY message_count DESC LIMIT 10", (first_day_of_last_month, last_day_of_last_month,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_received_thanks(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT users.first_name, users.last_name, messages.text FROM messages INNER JOIN users ON messages.sender_id = users.user_id WHERE messages.receiver_id = ?", (user_id,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_received_thanks_curr(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    # Получаем первый день текущего месяца
    first_day_of_current_month = datetime.date.today().replace(day=1)

    cursor.execute("SELECT users.first_name, users.last_name, messages.text FROM messages INNER JOIN users ON messages.sender_id = users.user_id WHERE messages.receiver_id = ? and messages.date > ?", (user_id, first_day_of_current_month))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_received_thanks_prev(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    # Получаем первый день прошлого месяца
    first_day_of_last_month = datetime.date.today().replace(day=1) - relativedelta(months=1)
    # Получаем последний день прошлого месяца
    last_day_of_last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)

    cursor.execute("SELECT users.first_name, users.last_name, messages.text FROM messages INNER JOIN users ON messages.sender_id = users.user_id WHERE messages.receiver_id = ? and messages.date >= ? and messages.date <= ?", (user_id, first_day_of_last_month, last_day_of_last_month))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_sent_thanks(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT users.first_name, users.last_name, messages.text FROM messages INNER JOIN users ON messages.receiver_id = users.user_id WHERE messages.sender_id = ?", (user_id,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_sent_thanks_curr(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    # Получаем первый день текущего месяца
    first_day_of_current_month = datetime.date.today().replace(day=1)

    cursor.execute("SELECT users.first_name, users.last_name, messages.text FROM messages INNER JOIN users ON messages.receiver_id = users.user_id WHERE messages.sender_id = ? and messages.date > ?", (user_id, first_day_of_current_month))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def get_sent_thanks_prev(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    # Получаем первый день прошлого месяца
    first_day_of_last_month = datetime.date.today().replace(day=1) - relativedelta(months=1)
    # Получаем последний день прошлого месяца
    last_day_of_last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)

    cursor.execute("SELECT users.first_name, users.last_name, messages.text FROM messages INNER JOIN users ON messages.receiver_id = users.user_id WHERE messages.sender_id = ? and messages.date >= ? and date <= ?", (user_id, first_day_of_last_month, last_day_of_last_month))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages

def add_user(user_id: int, first_name: str, last_name: str, speciality: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (user_id, first_name, last_name, speciality) VALUES (?, ?, ?, ?)",
                   (user_id, first_name, last_name, speciality))
    connection.commit()
    cursor.close()
    connection.close()

def update_user_info(user_id: int, first_name: str, last_name: str, speciality: str):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET first_name = ?, last_name = ?, speciality = ? WHERE user_id = ?",
                   (first_name, last_name, speciality, user_id))
    connection.commit()
    cursor.close()
    connection.close()