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
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение check_table users {es}')

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

    def add_link(self, id_user, link):

        now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute("INSERT OR IGNORE INTO links ('id_user', 'link',"
                            "'create_date') VALUES (?,?,?)",
                            (id_user, link,
                             now_date))

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

    def close(self):
        self.conn.close()
        print('Отключился от SQL BD')
