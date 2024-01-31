import tkinter as tk
import tkinter.messagebox as mb
import threading
import ccxt
import Bot
from time import sleep
from datetime import datetime


# Приложение.
class App:
    # Конструктор.
    def __init__(self):
        # Статус нажатия на кнопку.
        self.button_click_status = False
        # Поток обрабаьывающий логику.
        self.worker_thread = None

        # Создание окна и графического интерфейса.
        self.win = tk.Tk()
        logo = tk.PhotoImage(file="logo.png")
        self.win.iconphoto(False, logo)
        self.win.title("Crypto Assistant")
        self.win.geometry("400x500+500+200")
        self.win.resizable(False, False)

        # Версия приложения.
        self.version_label = tk.Label(self.win, text="Version 1.0")
        self.version_label.place(relx=1.0, rely=1.0, anchor="se")

        # Кнопка запуска программы.
        self.button = tk.Button(self.win, text="Start", width=18, height=3, font=("Arial", 18),
                                bg="#a7b5d1", bd=3, activebackground="#ced8eb",
                                highlightbackground="white", command=self.on_button_click)
        self.button.place(relx=0.5, rely=0.4, anchor="center")

        # Кнопка информации.
        self.btn_info = tk.Button(self.win, text="О программе",command=self.show_info)
        self.btn_info.place(relx=0.118, rely=0.97, anchor="center")

        # Статус работы программы.
        self.status_label = tk.Label(self.win, text="",
                                     font=("Arial", 16),
                                     fg="green")
        self.status_label.place(relx=0.5, rely=0.57, anchor="center")

        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.win.mainloop()


    def show_info(self):
        msg = "Версия программы: 1.0\nТаймфрейм: 15 минут\nКриптовалютные пары:\nBTC/USDT\nETH/USDT\nBNB/USDT\nSOL/USDT\nXRP/USDT\nTRX/USDT\nADA/USDT\nDOT/USDT"
        mb.showinfo("Информация", msg)




    # Действия при нажатии на кнопку.
    def on_button_click(self):
        self.button_click_status = not self.button_click_status

        if self.button_click_status:
            self.button.config(text="Stop")
            self.status_label.config(text="Программа работает...", fg="green")
            self.worker_thread = threading.Thread(target=self.work_controller)
            self.worker_thread.start()
        else:
            self.button.config(text="Start")
            self.status_label.config(text="Программа успешно завершена", fg="green")
            if self.worker_thread is not None:
                self.worker_thread.join()
                self.worker_thread = None
            print("Работа завершена, но окно открыто")


    # Действия при закрытии окна.
    def on_closing(self):
        self.button_click_status = False
        if self.worker_thread is not None:
            self.worker_thread.join()
        self.win.destroy()
        print("Программа закыта полностью")


    # Контроллер бизнес логики.
    def work_controller(self):
        Bot.send_message("Программа начала работать")
        while True:
            try:
                if (self.button_click_status == False):
                    break
                exchange = ccxt.binance()
                while self.button_click_status:
                    symbol = "BTC/USDT"
                    self.fetch_volume(symbol, exchange)
            except Exception as e:
                # status_label.config(text=f"{e}", fg="red")
                print("--------------------------------------")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"{e}")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("--------------------------------------")
                Bot.send_message(f"Произошла ошибка: {e}")

        Bot.send_message("Программа завершена")


    # Бизнес логика.
    # Получение данных.
    def fetch_volume(self, symbol, exchange):
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
            print(
                f"{datetime.fromtimestamp(candles[0][0] / 1000.0)} {candles[0][1]} {candles[0][2]} {candles[0][3]} {candles[0][4]} {candles[0][5]}")
        average_volume_5 = summ / 5.0
        print(f"Средний объём: {average_volume_5}")
        bot_sent_message_flag = False
        while True:
            if (self.button_click_status == False):
                break
            time = exchange.milliseconds() - 60000 * 1
            candles = None
            while True:
                candles = exchange.fetch_ohlcv(symbol, timeframe, since=time, limit=1)
                if (candles != None and len(candles) != 0):
                    break
            volume = candles[0][5]
            if (candles[0][0] == last_time):
                if (average_volume_5 * 3 <= volume and bot_sent_message_flag == False):
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"BTC/USDT \n Средний объём: {average_volume_5}   Объём на последней свече: {volume} \n Объём вырос в {volume / average_volume_5} раза")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    bot_message = f"BTC/USDT\nВремя: {datetime.fromtimestamp(candles[0][0] / 1000.0)}\nСредний объём: {round(average_volume_5, 2)}\nОбъём последней свечи: {round(volume, 2)}\nОбъём вырос в {round(volume / average_volume_5, 2)} раза"
                    print("Bot is ready")
                    Bot.send_message(bot_message)
                    print("Bot has sent message")
                    sleep(1)
                    bot_sent_message_flag = True
                else:
                    sleep(1)
                    continue
            else:
                break
