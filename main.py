import telebot
import dotenv
import os
import json
import database.connect_to_db as connect
import database.db as database
import schedule
import time
import buttons

def send_word(user_id):
    markup, random_word = buttons.random_word_markup(database)
    if user_id not in tempData:
        tempData[user_id] = {}
    else:
        bot.send_message(user_id, "Oh no! The last question that is toxic :(")
    tempData[user_id]["random_word"] = random_word
    bot.send_message(user_id, f"Translate this:<b>{random_word[1]}</b>", reply_markup=markup, parse_mode='html')


dotenv.load_dotenv()
tempData = {}
with open(os.getenv("JSON_FILE_PATH"), 'r') as file:
    json_data = json.load(file)
conn = connect.connectToDB()
database  = database.database(conn)
if conn != None:
    print(json_data["success_messages"]["database_successfully_connected"])
else:
    print(json_data["errors"]["database_connecting_error"])

bot = telebot.TeleBot(os.getenv("BOT_API_TOKEN"))

@bot.message_handler(commands=['start'])
def welcome(message):
    user = database.get_user_by_telegram_id(message.from_user.id)
    if user == None:
        sendMsg = bot.send_message(message.chat.id,json_data["welcome"])
        bot.register_next_step_handler(sendMsg, get_name_and_create_new_user)
    else:
        bot.send_message(message.chat.id, f"Hi,{user[2]}")
        send_word(message.chat.id)

def get_name_and_create_new_user(message):
    err = database.create_new_user(message.from_user.id, message.text)
    if err == None:
        sendMsg = bot.send_message(message.chat.id, json_data["errors"]["creating_new_user_error"])
        bot.register_next_step_handler(sendMsg, welcome)
        return
    bot.send_message(message.chat.id, f"Welcome {message.text}")
    send_word(message.chat.id)

@bot.message_handler(commands=['add'])
def add_new_word(message):
    tempData[message.from_user.id] = {}
    sendMsg = bot.send_message(message.chat.id, text=json_data["new_word"])
    bot.register_next_step_handler(sendMsg, get_word_and_send_translated_word)

def get_word_and_send_translated_word(message):
    tempData[message.from_user.id]["word"] = message.text
    sendMsg = bot.send_message(message.chat.id, json_data["translated_word"])
    bot.register_next_step_handler(sendMsg, get_translated_word_and_save_data)

def get_translated_word_and_save_data(message):
    tempData[message.from_user.id]["translated_word"] = message.text
    tempData[message.from_user.id]["category_id"] = 1
    err = database.create_new_word(tempData[message.from_user.id])
    if err == None:
        sendMsg = bot.send_message(message.chat.id, json_data["errors"]["creating_new_word"])
        bot.register_next_step_handler(sendMsg, add_new_word)
        return
    bot.send_message(message.chat.id, "Added")
    del tempData[message.from_user.id]

@bot.callback_query_handler(func= lambda call: call.data.startswith("answer-"))
def answer_the_question(call):
    answer = call.data.split("-")[1]
    try:
        if int(answer) == tempData[call.message.chat.id]["random_word"][0]:
            bot.send_message(call.message.chat.id, "Answer is correct!")
            del tempData[call.message.chat.id]
        else:
            bot.send_message(call.message.chat.id, "Incorrect! Try again")
    except KeyError:
        bot.send_message(call.message.chat.id, "You already answer this question :)")


def send_message_to_users():
    users = database.get_all_users()
    for user in users:
        try:
            send_word(user[1])
        except Exception as e:
            print(f"Error sending message to user {user[1]}: {e}")

schedule.every().minute.do(send_message_to_users)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

import threading
threading.Thread(target=run_schedule).start()


print("Bot is running...")
bot.infinity_polling()

