import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)  # Подключаемся к БД, если ее нет то создаем

    def execute(
            self,
            sql: str,
            parameters: tuple = None,
            fetchone=False,  # fetchone - забрать 1 значение в кортеже tuple((),)
            fetchall=False,  # fetchall - забрать все значения в списке списков ((),(),(),),
            fetchmany=False,  # fetchmany - забрать все значения указав кол-во возвращаемых строк
            commit=False,  # commit - хотим ли мы сделать коммит
    ):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        connection.set_trace_callback(logger)

        cursor = connection.cursor()
        # "SELECT * FROM Users WHERE id=1"
        # Пример команды с параметрами
        # "INSERT INTO User (id, username, email) VALUES(?, ?, ?)"
        data = None
        cursor.execute(sql, parameters)  # Исполняем какую-то команду c параметрами
        if commit:
            connection.commit()  # Сохраняем изменения в БД
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        if fetchmany:
            data = cursor.fetchmany()

        connection.close()  # Закрываем подключение к БД
        return data

    def create_table_users(self):
        sql = "CREATE TABLE IF NOT EXISTS users (" \
              "id INTEGER PRIMARY KEY NOT NULL," \
              "user_id INTEGER NOT NULL UNIQUE," \
              "username TEXT NOT NULL UNIQUE," \
              "email TEXT" \
              ");"
        self.execute(sql, commit=True)

    def create_table_photo(self):
        sql = "CREATE TABLE IF NOT EXISTS photo (" \
              "id INTEGER PRIMARY KEY NOT NULL," \
              "user_id INTEGER NOT NULL," \
              "photo TEXT NOT NULL, " \
              "like_dislike INTEGER," \
              "FOREIGN KEY (user_id)  REFERENCES users (user_id) ON DELETE CASCADE" \
              ");"
        self.execute(sql, commit=True)

    def add_user(self, user_id: int, username: str, email: str = None):
        # Добавляем нового пользователя
        sql = "INSERT INTO users(user_id, username, email) VALUES(?, ?, ?)"
        # Указываем параметры
        parameters = (user_id, username, email)
        # Создаем новую запись в БД
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = "SELECT * FROM users"
        return self.execute(sql, fetchall=True)

    # Форматируем запрос sql для подстановки в select_user
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        # Пример параметра для получения пользователя:
        # {"id": 1}
        # {"user_id": 12345}
        # {"username": "John"}
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def update_username(self, username, id=None, user_id=None):
        # Пример sql запроса "UPDATE Users SET username=new_name WHERE user_id=12345 or id=1"
        sql = "UPDATE users SET username=? WHERE user_id=? or id=?"
        return self.execute(sql, parameters=(username, id, user_id), commit=True)

    def update_email(self, email, id=None, user_id=None):
        # Пример sql запроса "UPDATE Users SET email=mail@gmail.com WHERE id=12345"
        sql = "UPDATE users SET email=? WHERE user_id=? or id=?"
        return self.execute(sql, parameters=(email, id, user_id), commit=True)

    # Удаляем одного пользователя
    def delete_user(self, id=None, user_id=None):
        return self.execute(
            "DELETE FROM users WHERE user_id=? or id=?",
            parameters=(id, user_id), commit=True
        )

    # Удаляем всех пользователе
    def delete_users(self):
        self.execute("DELETE FROM users WHERE TRUE")

    def add_photo(self, user_id: int, photo: str, like_dislike: str = 0):
        # Добавляем новое фото пользователю
        sql = "INSERT INTO photo (user_id, photo, like_dislike) VALUES (?, ?, ?)"
        # Указываем параметры
        parameters = (user_id, photo, like_dislike)
        # Создаем новую запись в БД
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_user_photo(self, user_id: int):
        sql = "SELECT * FROM photo WHERE user_id=?"
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def update_like_dislike(self, photo: str, like_dislike: int):
        sql = "UPDATE photo SET like_dislike=? WHERE photo=?"
        return self.execute(sql, parameters=(like_dislike, photo), commit=True)

    def clear_all_user_photo(self, user_id: int):
        return self.execute(
            "DELETE FROM photo WHERE user_id=?",
            parameters=(user_id,), commit=True
        )


def logger(statement):
    print(f"""
-------------------------------------------------------------------
Executing:
{statement}
-------------------------------------------------------------------
""")
