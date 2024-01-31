# Бибилиотека python-telegram-bot 13.0 , так как здесь более удобная работа с ботом, которая не занимает целый поток.
from telegram import Bot

# Данные бота.
bot_token = '6500188821:AAET5x2AOab8toa31NiL2V_u3LuOKhkXSBA'
chat_id = '1180171947'

# Отправка сообщения для бота.
def send_message(message):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id, text=message)

