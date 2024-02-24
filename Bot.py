# Бибилиотека python-telegram-bot 13.15 , так как здесь более удобная работа с ботом, которая не занимает целый поток.
from telegram import Bot


# Данные бота.
bot_token = '6500188821:AAFhCttcfBMmEdES3gjlwkWg9JcXrRHewSI'
# chat_id = '-4129403273'
chat_id = '1180171947'

# Отправка сообщения от бота.
def send_message(message):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id, text=message)