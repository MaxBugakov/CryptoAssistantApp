import socket
import ccxt
from datetime import datetime


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
def fetch_volume(symbol):
    exchange = ccxt.binance()  # Используйте свою биржу, если не Binance
    timeframe = '15m'
    summ = 0
    print("-----Последние 5 свечек-----")
    for i in range(5):
        time = exchange.milliseconds() - 60000 * 15 * (i + 2)
        candles = exchange.fetch_ohlcv(symbol, timeframe, since=time, limit=1)
        volume = candles[0][5]
        summ += volume
        print(f"{datetime.fromtimestamp(candles[0][0] / 1000.0)} {candles[0][1]} {candles[0][2]} {candles[0][3]} {candles[0][4]} {candles[0][5]}")
    print(f"Средний объём: {summ / 5}")
    time = exchange.milliseconds() - 60000 * 15
    candles = exchange.fetch_ohlcv(symbol, timeframe, since=time, limit=1)
    print(f"{datetime.fromtimestamp(candles[0][0] / 1000.0)} {candles[0][1]} {candles[0][2]} {candles[0][3]} {candles[0][4]} {candles[0][5]}")
