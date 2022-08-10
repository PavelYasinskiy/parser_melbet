import time

import telebot
from telebot import types
from decouple import config

from line.get_games_decode_line import find_all_games_line
from live.get_game_live import find_all_games_live

TOKEN_BOT = config('TOKEN_BOT')
bot = telebot.TeleBot(TOKEN_BOT)




bot.send_message(chat_id=349766837, text=f"Привет, ждем сигналов!")
while True:
    start_time = time.time()
    try:
        try:
            find_all_games_line()
        except TypeError:
            print("Ошибка в лайне")
        while time.time()-start_time < 7200:
            time.sleep(5)
            all_signals = find_all_games_live()
            print(all_signals)
            for _, signal in enumerate(all_signals):
                if signal is not None:
                    bot.send_message(chat_id=349766837, text=f"Лига: {signal[2]}\n"
                                                                        f"ЛигаEN: {signal[1]}\n"
                                                                        f"Матч: {signal[4]}-{signal[6]}\n"
                                                                        f"Тоталы prematch:\n{signal[8]}Б {signal[9]} "
                                                                        f"- {signal[10]}М {signal[11]}\n"
                                                                        f"{signal[12]}")
                    time.sleep(2)
    except Exception:
        pass



