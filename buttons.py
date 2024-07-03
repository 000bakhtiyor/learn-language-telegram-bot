from telebot.types import *
import random 

def random_word_markup(database):
    random_words = database.get_random_words()
    random_word = random_words[random.randint(0,3)]
    markup = InlineKeyboardMarkup()

    for word in random_words:
        markup.add(
            InlineKeyboardButton(
                word[2], 
                callback_data=f"answer-{word[0]}"
            )
        )

    return markup, random_word
    