import tkinter as tk
import threading
from time import sleep
import BusinessLogic
from telegram import Bot

# Контроллер бизнесс логики.
def work():
    global button_click_status
    try:
        BusinessLogic.check_network_connection()
        while button_click_status:
            symbol = "BTC/USDT"
            BusinessLogic.fetch_volume(symbol)
    except Exception as e:
        status_label.config(text=f"{e}", fg="red")


# Действия при нажатии на кнопку.
def on_button_click():
    global button_click_status, worker_thread
    button_click_status = not button_click_status

    if button_click_status:
        button.config(text="Stop")
        status_label.config(text="Программа работает...", fg="green")
        worker_thread = threading.Thread(target=work)
        worker_thread.start()
    else:
        button.config(text="Start")
        status_label.config(text="Программа успешно завершена", fg="green")
        if worker_thread is not None:
            worker_thread.join()
            worker_thread = None
        print("Работа завершена, но окно открыто")


# Действия при закрытии окна.
def on_closing():
    global button_click_status
    button_click_status = False
    if worker_thread is not None:
        worker_thread.join()
    win.destroy()
    print("Программа закыта полностью")


# Глобальные переменные.
button_click_status = False
worker_thread = None


def bot_messege_set(textt):
    bot.send_message(chat_id, text=textt)

bot_token = '6500188821:AAET5x2AOab8toa31NiL2V_u3LuOKhkXSBA'
bot = Bot(token=bot_token)
chat_id = '1180171947'

# Main.
if __name__ == "__main__":
    # Создание окна.
    win = tk.Tk()
    logo = tk.PhotoImage(file="logo.png")
    win.iconphoto(False, logo)
    win.title("Crypto Assistant")
    win.geometry("400x500+500+200")
    win.resizable(False, False)

    # Версия.
    version_label = tk.Label(win, text="Version 1.0")
    version_label.place(relx=1.0, rely=1.0, anchor="se")

    # Кнопка.
    button = tk.Button(win, text="Start", width=18, height=3, font=("Arial", 18),
                       bg="#a7b5d1", bd=3, activebackground="#ced8eb",
                       highlightbackground="white", command=on_button_click)
    button.place(relx=0.5, rely=0.4, anchor="center")

    # Статус работы программы.
    status_label = tk.Label(win, text="",
                            font=("Arial", 16),
                            fg="green",
                            )
    status_label.place(relx=0.5, rely=0.57, anchor="center")

    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()






