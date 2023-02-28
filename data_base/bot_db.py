import sqlite3
from bot_config import bot


def sql_start():
    global conn, cursor
    conn = None
    try:
        conn = sqlite3.connect("database.db")
        print("successfully connection to database")
    except Error as e:
        print(e)

    cursor = conn.cursor()
    # conn.execute("DROP TABLE user_data")
    # conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_data(
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT,
    photo_id TEXT)""")
    conn.commit()


async def sql_add_data(state):
    async with state.proxy() as data:
        # get quantity of records with given login
        cursor.execute("select count(*) from user_data where login = ?", [data["login"]])
        # get all records from executed query
        count = cursor.fetchall()[0][0]
        # if no records add one
        if count < 1:
            cursor.execute("""
            INSERT INTO user_data (login, first_name, last_name, phone_number, photo_id)
            VALUES (?,?,?,?,?)""", tuple(data.values()))
            conn.commit()
        # if have record - update
        else:
            cursor.execute(f"""
            update user_data
            set first_name = ?, last_name = ?, phone_number = ?, photo_id = ?
            where login = ?""", [data["first_name"], data["last_name"], data["phone_number"], data["photo_id"], data["login"]])
            conn.commit()


async def sql_read(message):
    for lis in cursor.execute("SELECT * FROM user_data").fetchall():
        await bot.send_photo(message.from_user.id, lis[5], f"{lis[1]}, {lis[2]}, {lis[3]}, {lis[4]}")


async def sql_delete(login):
    # print(login)
    cursor.execute(f"""
    delete from user_data
    where login = ?""", [login])


async def sql_get_photo_id(login):
    print(login)
    cursor.execute("""
    select photo_id
    from user_data
    where login = ?""", [login])
    user_photo_id = cursor.fetchone()[0]
    print(user_photo_id)
    return user_photo_id





