from utils.db_api.sqlite import Database

db = Database()


def test_user():
    db.create_table_users()
    db.create_table_photo()
    users = db.select_all_users()
    print(f"До добавления users: {users}")
    db.add_user(1234, "One", "email@email.com")
    db.add_user(223435, "Two", "email_2@email.com")
    users = db.select_all_users()
    print(f"После добавления users: {users}")
    user = db.select_user(username="One", id=1)
    not_user = db.select_user(username="Oleg")
    print(not_user)  # None
    print(f"Получил user: {user}")


test_user()
