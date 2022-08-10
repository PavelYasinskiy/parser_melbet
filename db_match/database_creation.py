import sqlite3

def create_info(game_id: int) -> None:
    """
    Создает базу данных и добавляет пользователя.

    :param user_id: int пользовательский id
    """

    with sqlite3.connect("db_match/prematch.db") as game_data:
        cur = game_data.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS games(game_id INTEGER UNIQUE,
                                                        liga_eng TEXT,
                                                        liga_ru TEXT,
                                                        liga_id INTEGER,
                                                        home TEXT,
                                                        home_id INTEGER,
                                                        guest TEXT,
                                                        guest_id INTEGER,
                                                        total_mid_b INTEGER,
                                                        total_coef_b INTEGER,
                                                        total_mid_m INTEGER,
                                                        total_coef_m INTEGER,
                                                        total_min INTEGER
                                                        )""")
        try:
            cur.execute(f'''INSERT INTO games(game_id) VALUES({game_id})''')
        except sqlite3.IntegrityError:
            pass
        finally:
            game_data.commit()



def add_info(column: str, value: any, game_id: int) -> None:
    """
    Добавляет в базу данных информацию пользователя.

    :param column: str Колонка в которую добавляем информацию
    :param value: any Новое значение колонки
    :param game_id: int ID игры
    """
    with sqlite3.connect('db_match/prematch.db') as game_data:
        cur = game_data.cursor()
        cur.execute(f"""UPDATE games SET {column} = ? WHERE game_id = ?""", (value, game_id))
        game_data.commit()



def show_info(home_id: int, guest_id: int, liga_id: int) -> list:
    """
    Возвращает список доступной информации по пользователю.
    :param user_id: int ID игры
    :return: list [command,city_ID,city_name,price_min,price_max,checkIn_date,checkOut_date,distance_min
     distance_max,hotel_count, photo_count, history ]
    """
    with sqlite3.connect("db_match/prematch.db") as game_data:
        cur = game_data.cursor()
        cur.execute(f"""SELECT * FROM games WHERE liga_id = {liga_id}
                                              AND home_id = {home_id} 
                                              AND guest_id = {guest_id} ORDER BY game_id DESC LIMIT 1""")
        ret = cur.fetchall()
        fun = list(map(lambda x: str(x), ret[0]))
        return fun

def clean_db():
    with sqlite3.connect('db_match/prematch.db') as game_data:
        cur = game_data.cursor()
        cur.execute(f"""DELETE FROM games """)
        game_data.commit()



        # select * from  games where home_id = 3705429 ORDER BY game_id DESC limit 1