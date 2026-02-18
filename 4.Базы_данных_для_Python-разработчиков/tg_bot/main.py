import telebot
import random
from telebot import types
from database import (add_user, get_random_word, get_wrong_words,
                      add_word_to_db, get_user_words, delete_word_from_db,
                      get_all_common_words, toggle_word_exclusion, get_excluded_words)

token = '8364052922:AAFXvGnFjcbtzSkQmuJohD5AyBIOEielp8o'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    cid = message.chat.id
    add_user(cid)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_next = types.KeyboardButton('Начать')
    btn_add = types.KeyboardButton('Добавить слово')
    btn_del = types.KeyboardButton('Удалить слово')
    btn_exclude = types.KeyboardButton('Настройка общих слов ⚙️')

    markup.add(btn_next)
    markup.add(btn_exclude)
    markup.row(btn_add, btn_del)
    bot.send_message(cid, "Привет! Давай попрактикуемся в английском.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Выйти')
def handle_exit(message):
    welcome(message)


@bot.message_handler(func=lambda message: message.text in ['Начать', 'Дальше'])
def next_word(message):
    cid = message.chat.id
    word_pair = get_random_word(cid)
    if not word_pair:
        bot.send_message(cid, "Доступные слова закончились. Включите общие слова или добавьте свои!")
        return
    target, correct = word_pair
    others = get_wrong_words(target)
    options = [correct] + others
    random.shuffle(options)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(opt) for opt in options]
    markup.add(*buttons)
    markup.row(types.KeyboardButton('Выйти'), types.KeyboardButton('Дальше'))

    msg = bot.send_message(cid, f"Как переводится слово: {target}?", reply_markup=markup)
    bot.register_next_step_handler(msg, check_answer, correct, target)


def check_answer(message, correct_answer, target_word):
    cid = message.chat.id
    user_answer = message.text
    if user_answer == 'Выйти':
        welcome(message)
    elif user_answer == 'Дальше':
        next_word(message)
    elif user_answer == correct_answer:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Выйти'), types.KeyboardButton('Дальше'))
        bot.send_message(cid, "Отлично! ✅ Верно.", reply_markup=markup)
    else:
        msg = bot.send_message(cid, f"Не совсем. Попробуй еще раз! Как переводится {target_word}? ❌")
        bot.register_next_step_handler(msg, check_answer, correct_answer, target_word)


# Логика добавления/удаления личных слов
@bot.message_handler(func=lambda message: message.text == 'Добавить слово')
def add_word(message):
    msg = bot.send_message(message.chat.id, "Введите слово на английском:")
    bot.register_next_step_handler(msg, process_word_step)


def process_word_step(message):
    target = message.text.strip()
    msg = bot.send_message(message.chat.id, f"Как переводится '{target}'?")
    bot.register_next_step_handler(msg, save_word_step, target)


def save_word_step(message, target):
    add_word_to_db(message.chat.id, target, message.text.strip())
    bot.send_message(message.chat.id, "Слово добавлено! ✨")
    welcome(message)


@bot.message_handler(func=lambda message: message.text == 'Удалить слово')
def show_words_to_delete(message):
    cid = message.chat.id
    words = get_user_words(cid)
    if not words:
        bot.send_message(cid, "Ваш словарь пуст.")
        return
    markup = types.InlineKeyboardMarkup()
    for w in words:
        markup.add(types.InlineKeyboardButton(text=f"🗑 {w}", callback_data=f"del_{w}"))
    bot.send_message(cid, "Выберите слово для удаления:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('del_'))
def handle_delete(call):
    word = call.data.split('_')[1]
    delete_word_from_db(call.message.chat.id, word)
    bot.answer_callback_query(call.id, text="Удалено")
    bot.send_message(call.message.chat.id, f"Слово '{word}' удалено.")


# Логика исключения/включения общих слов
@bot.message_handler(func=lambda message: message.text == 'Настройка общих слов ⚙️')
def settings_common_words(message):
    cid = message.chat.id
    all_words = get_all_common_words()
    excluded = get_excluded_words(cid)

    markup = types.InlineKeyboardMarkup()
    for w in all_words:
        icon = "❌" if w in excluded else "✅"
        markup.add(types.InlineKeyboardButton(text=f"{icon} {w}", callback_data=f"toggle_{w}"))
    bot.send_message(cid, "Нажмите на слово, чтобы включить/выключить его в тренировке:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('toggle_'))
def handle_toggle(call):
    cid = call.message.chat.id
    word = call.data.split('_')[1]
    action = toggle_word_exclusion(cid, word)

    # Обновляем кнопки
    all_words = get_all_common_words()
    excluded = get_excluded_words(cid)
    markup = types.InlineKeyboardMarkup()
    for w in all_words:
        icon = "❌" if w in excluded else "✅"
        markup.add(types.InlineKeyboardButton(text=f"{icon} {w}", callback_data=f"toggle_{w}"))

    bot.answer_callback_query(call.id, text="Обновлено")
    bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.message_id, reply_markup=markup)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)