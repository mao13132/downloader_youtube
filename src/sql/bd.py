import datetime

import sqlite3

from datetime import datetime


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"users (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_user TEXT, "
                                f"login TEXT, "
                                f"status TEXT DEFAULT new, "
                                f"join_date DATETIME, "
                                f"last_time DATETIME DEFAULT 0, "
                                f"other TEXT,"
                                f"count_down INT DEFAULT 0,"
                                f"down_status BOOLEAN DEFAULT 0)")

        except Exception as es:
            print(f'SQL исключение check_table users {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"response_word (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"search_word TEXT, "
                                f"response_type TEXT, "
                                f"response_text TEXT, "
                                f"response_file TEXT, "
                                f"tag TEXT, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение response_word {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"links (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_user TEXT, "
                                f"link TEXT, "
                                f"create_date DATETIME DEFAULT 0, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение links {es}')

    def check_or_add_user(self, id_user, login):

        result = self.cursor.execute(f"SELECT * FROM users WHERE id_user='{id_user}'")

        response = result.fetchall()

        if response == []:
            now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute("INSERT OR IGNORE INTO users ('id_user', 'login',"
                                "'join_date') VALUES (?,?,?)",
                                (id_user, login,
                                 now_date,))

            self.conn.commit()

            return True

        return False

    def get_user_data_from_id(self, id_user):
        try:

            result = self.cursor.execute(f"SELECT * FROM users "
                                         f"WHERE id_user = '{id_user}'")

            response = result.fetchall()

            response = response[0]


        except Exception as es:
            print(f'Ошибка SQL get_user_data_from_id: {es}')
            return False

        return response

    def update_user_key(self, id_user, key, value):
        try:
            self.cursor.execute(f"UPDATE users SET {key} = '{value}' WHERE id_user = '{id_user}'")
            self.conn.commit()
            return True
        except Exception as es:
            print(f'SQL Ошибка при обновления языка update_user_key "{es}"')
            return False

    def add_link(self, id_user, link):

        now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute("INSERT OR IGNORE INTO links ('id_user', 'link',"
                            "'create_date') VALUES (?,?,?)",
                            (id_user, link,
                             now_date))

        self.conn.commit()

        return self.cursor.lastrowid

    def add_response_msg(self, search_word, _type_msg, _sql_file_patch, _text_response, tag):
        self.cursor.execute("INSERT OR IGNORE INTO response_word ('search_word', 'response_type',"
                            "'response_file', 'response_text', 'tag') VALUES (?,?,?,?,?)",
                            (search_word, _type_msg,
                             _sql_file_patch, _text_response, tag))

        self.conn.commit()

        return self.cursor.lastrowid

    def get_link(self, id_pk):
        try:

            result = self.cursor.execute(f"SELECT link FROM links "
                                         f"WHERE id_pk = '{id_pk}'")

            response = result.fetchall()

            response = response[0][0]


        except Exception as es:
            print(f'Ошибка SQL get_link: {es}')
            return False

        return response

    def get_all_users(self):

        result = self.cursor.execute(f"SELECT * FROM users")

        response = result.fetchall()

        return response

    def get_response_word_from_id_pk(self, id_pk):
        try:

            result = self.cursor.execute(f"SELECT * FROM response_word "
                                         f"WHERE id_pk = '{id_pk}'")

            response = result.fetchall()

            response = response[0]


        except Exception as es:
            print(f'Ошибка SQL get_response_word_from_id_pk: {es}')
            return False

        return response

    def plus_count_down(self, id_user):

        result = self.cursor.execute(f"SELECT count_down FROM users WHERE id_user='{id_user}'")

        response = result.fetchall()

        if response != []:

            try:
                response = response[0][0]
            except:
                return False

            try:
                response = int(response) + 1
            except:
                return False

            result = self.cursor.execute(f"UPDATE users SET count_down = '{response}' WHERE id_user='{id_user}'")

            self.conn.commit()

            return True

        return False

    def close(self):
        self.conn.close()
        print('Отключился от SQL BD')
