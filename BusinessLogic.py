import socket
import ccxt
from datetime import datetime
from time import sleep
import main


# Проверка соединения.
def check_network_connection():
    host = "www.google.com"
    port = 80
    timeout = 5  # время ожидания в секундах

    try:
        # Создаем сокет и пытаемся подключиться к хосту и порту
        socket.create_connection((host, port), timeout=timeout)
    except Exception as e:
        raise Exception(f"Ошибка соединения:\n {e}")


# Получение данных.
def fetch_volume(symbol, exchange, iteration_counter):
    print(iteration_counter)
    if (iteration_counter % 20 == 0):
        main.bot_messege_set("Прошло 20 минут")
        print("Бот отправил: Прошло 20 минут")
    timeframe = '1m'
    summ = 0
    print("-----Последние 6 свечек-----")
    last_time = None
    last_volume = 0
    # bot_message = ""
    for i in range(6):
        time = exchange.milliseconds() - 60000 * (i + 1)
        candles = exchange.fetch_ohlcv(symbol, timeframe, since=time, limit=1)
        volume = candles[0][5]
        if (i != 0):
            summ += volume
        if (i == 0):
            last_time = candles[0][0]
            last_volume = candles[0][5]
        print(f"{datetime.fromtimestamp(candles[0][0] / 1000.0)} {candles[0][1]} {candles[0][2]} {candles[0][3]} {candles[0][4]} {candles[0][5]}")
    average_volume_5 = summ/5.0
    print(f"Средний объём: {average_volume_5}")
    bot_sent_message_flag = False
    while True:
        time = exchange.milliseconds() - 60000 * 1
        candles = None
        while True:
            candles = exchange.fetch_ohlcv(symbol, timeframe, since=time, limit=1)
            if (candles != None and len(candles) != 0):
                break
        # print(candles)
        volume = candles[0][5]
        # print(f"{datetime.fromtimestamp(candles[0][0] / 1000.0)} {candles[0][1]} {candles[0][2]} {candles[0][3]} {candles[0][4]} {candles[0][5]}")
        # print(f"{last_time} - {datetime.fromtimestamp(last_time / 1000.0)}")
        # print(f"{candles[0][0]} - {datetime.fromtimestamp(candles[0][0] / 1000.0)}")
        if (candles[0][0] == last_time):
            if (average_volume_5 * 3 <= volume and bot_sent_message_flag == False):
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"BTC/USDT \n Средний объём: {average_volume_5}   Объём на последней свече: {volume} \n Объём вырос в {volume / average_volume_5} раза")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                bot_message = f"BTC/USDT\nВремя: {datetime.fromtimestamp(candles[0][0] / 1000.0)}\nСредний объём 5: {average_volume_5}\nОбъём: {volume}\nОбъём вырос в {volume / average_volume_5} раза"
                print("Bot is ready")
                main.bot_messege_set(bot_message)
                print("Bot has sent message")
                sleep(2)
                bot_sent_message_flag = True
            else:
                sleep(2)
                continue
        else:
            break
