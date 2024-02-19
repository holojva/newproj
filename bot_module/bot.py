# import os
# import telebot

# print(os.environ.get("TOKEN"))
# token = os.environ.get("TOKEN")

# bot = telebot.TeleBot("6716709020:AAF_77A_Bu3_woJBYnpZizM8X4kZGe2DjJs")

# chat_id = "1269033016"

# def send_task_notification(text) :
#     bot.send_message(1269033016,text)
# bot.infinity_polling()

import telebot
import requests
token='6716709020:AAF_77A_Bu3_woJBYnpZizM8X4kZGe2DjJs'
print("print")
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет ✌️ ")
  r = requests.get(f'http://127.0.0.1:8000/chat_id/?chat_id={message.chat.id}')
  print("print test")
bot.infinity_polling()