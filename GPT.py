TOKEN = '7325488277:AAGKg0tmAL__EtG6god17vm4_YYzOthwZyM'

import telebot
from telebot import types
import hashlib

def hash_username(username):

    hash = hashlib.sha256(username.encode()).hexdigest()
    for i in range(5, 256):
        if not (hash[:i] in members_hash.keys()):
            members_hash[username] = hash[:i]
            members_hash[hash[:i]] = username
            break


bot = telebot.TeleBot(TOKEN)
members = set(['iamtima','Liza_shysha'])
members_id = {'iamtima': 911405448, 911405448: 'iamtima', 'Liza_shysha': 1960819968, 1960819968: 'Liza_shysha'}
members_hash = {'iamtima': '1b874', '1b874': 'iamtima', 'Liza_shysha': 'ee99e', 'ee99e': 'Liza_shysha'}
startup_313_id = 6200853679
#print('НАЧАЛО', members,members_id,members_hash)


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    text = message.text
    print(text)
    username = message.from_user.username
    if not (username in members):
        members.add(username)
        members_id[username] = message.from_user.id
        members_id[message.from_user.id] = username
        hash_username(username)
    if "/start" in text:
        if text == "/start":
            hash_admin = members_hash[message.from_user.username]
            link = f't.me/{bot.get_me().username}?start={hash_admin}'
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('🔗 Поделиться ссылкой',
                                                  url=f'https://t.me/share/url?url=Пришли%20мне%20анонимное%20сообщение:%0A%0A👉%20{link}'))
            bot.send_message(message.from_user.id,
                             f"Начни получать анонимные сообщения прямо сейчас 🚀\n\nТвоя ссылка:\n👉 {link}\n\nРазмести эту ссылку ☝️ в описании профиля Telegram/TikTok/Instagram, или отправь в свой канал с помощью кнопки 👇, чтобы начать получать сообщения",
                             reply_markup=markup)
        else:
            if text[7]=='-':
                chat_id = message.chat.id
                message_id = message.message_id
                bot.delete_message(chat_id, message_id)
                bot.delete_message(chat_id, message_id - 1)
                bot.delete_message(chat_id, message_id - 2)
                id = members_id[members_hash[text[8:]]]
            else:
                id = members_id[members_hash[text[7:]]]
            bot.send_message(message.from_user.id, f"Напишите ваше анонимное сообщение:")
            bot.register_next_step_handler(message, on_click, id)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю")
    #print(text, message.from_user.username, members_id, members_hash)

def on_click(message, id):
    #print(message)
    b = True
    if message.content_type == 'text':
        message_2 = message.text
        bot.send_message(id, f"У вас новое анонимное сообщение:\n{message_2}")
        bot.send_message(
            startup_313_id,
            f"новое анонимное сообщение к {members_id[id]} от {message.from_user.username}:\n{message_2}"
        )
    else:
        if message.content_type == 'sticker':
            message_2 = message.sticker.file_id
            bot.send_message(id, "У вас новое анонимное сообщение:")
            bot.send_sticker(id, message_2)
            bot.send_message(startup_313_id,
                             f"новое анонимное сообщение к {members_id[id]} от {message.from_user.username}:")
            bot.send_sticker(startup_313_id, message_2)
        elif message.content_type == 'document':
            message_2 = message.document.file_id
            print(message_2)
            bot.send_message(id, "У вас новое анонимное сообщение:")
            bot.send_voice(id, message_2)
            bot.send_message(startup_313_id,
                             f"новое анонимное сообщение к {members_id[id]} от {message.from_user.username}:")
            bot.send_voice(startup_313_id, message_2)

        else:
            bot.send_message(message.from_user.id, 'К сожалению я не могу это отправить')
            b = False
    #print(message, '\n', message_2)
    if b:
        bot.send_message(startup_313_id,
                         f"{message.from_user.username}:\n{message.from_user.first_name} {message.from_user.last_name} {message.from_user.language_code}")
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id = types.KeyboardButton(f'/start')
        markup_reply.add(item_id)

        chat_id = message.chat.id
        message_id = message.message_id
        bot.delete_message(chat_id, message_id)
        bot.delete_message(chat_id, message_id - 1)

        link = f't.me/{bot.get_me().username}?start=-{members_hash[members_id[id]]}'
        markup_reply = types.InlineKeyboardMarkup()
        markup_reply.add(types.InlineKeyboardButton('✍️ Отправить ещё',
                                              url=link))
        bot.send_message(message.from_user.id, 'Ваше сообщение отправлено', reply_markup=markup_reply)
        hash_admin = members_hash[message.from_user.username]
        link = f't.me/{bot.get_me().username}?start={hash_admin}'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('🔗 Поделиться ссылкой',
                                              url=f'https://t.me/share/url?url=Пришли%20мне%20анонимное%20сообщение:%0A%0A👉%20{link}'))
        bot.send_message(message.from_user.id,
                         f"Начни получать анонимные сообщения прямо сейчас 🚀\n\nТвоя ссылка:\n👉 {link}\n\nРазмести эту ссылку ☝️ в описании профиля Telegram/TikTok/Instagram, или отправь в свой канал с помощью кнопки 👇, чтобы начать получать сообщения",
                         reply_markup=markup)


bot.polling(none_stop=True, interval=0)
