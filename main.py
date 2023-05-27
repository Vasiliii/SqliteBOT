import telebot
import config
import sqlite3

from sqlite3.dbapi2 import connect
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
name = None


@bot.message_handler(commands=['start', 'create'])
def welcome(message):
    
    sti = open('static/AnimatedSticker.tgs', 'rb')
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id int primary key,
        admin int pimary key,
        name varchar(70),
        pass varchar(20)
        )""")
    conn.commit()
    
    cur.close()
    conn.close()

    
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    murkup.add(config.MainBut0, config.MeinBut1)

    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, f'Привет. Я бот работающий с базой данных SQLite3', parse_mode = 'html', reply_markup= murkup)
    
@bot.message_handler(content_types=['text'])
def reserch(message):
    if message.text == 'Регистрация':
        
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()
    
        people_id = message.chat.id 
        cur.execute(f"""SELECT id FROM users WHERE id = {people_id}""")
        
        data = cur.fetchone()
        if data is None:
            bot.send_message(message.chat.id, f'Придумайте имя')
            bot.register_next_step_handler(message, user_name)
        else:
            bot.send_message(message.chat.id, "Вы уже зарегистрированны")
    
        cur.close()
        conn.close()
    
    if message.text == 'Авторизация':
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()
    
        people_id = message.chat.id 
        cur.execute(f"""SELECT id FROM users WHERE id = {people_id}""")
        
        data = cur.fetchone()
        if data is None:
            bot.send_message(message.chat.id, f'Извините мы не нашли ваш id.\n Возможно вы сменили аккаунт в телеграм\n Пожалйста введите ваше имя')
            bot.register_next_step_handler(message, user_auto)
        else:
            bot.send_message(message.chat.id, "Вы успешно вошли")
    
    cur.close()
    conn.close()
    
def user_auto(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, user_auto_pass)
        
def user_name(message):
    global name 
    name = message.text.strip()
    bot.send_message(message.chat.id, f'Придумайте пароль')
    bot.register_next_step_handler(message, user_pass)

def user_auto_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    
    cur.execute(f"SELECT name FROM users WHERE name = '%s'" % (name) )
    data = cur.fetchone()
    cur.execute(f"SELECT pass FROM users WHERE pass = '%s'" % (password) )
    data1 = cur.fetchone()
    
    if data != None and data1 != None:
        global people_id
        people_id = message.chat.id 
        markup = types.InlineKeyboardMarkup()
        
        markup.add(config.updateBut)
    
        bot.send_message(people_id, "Вы успешно авторизовались!🥳", reply_markup=markup)
    else:
        bot.send_message(people_id, f"Что-то пошло не так возможно неверный логин или пароль.\nЕсли вы забыли пароль обратитесь к администратору😢😢😢")

@bot.callback_query_handler(func= lambda call: True)
def updata(call):
    global people_id
    
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    
    cur.execute("UPDATE users SET id = ? WHERE name = ?", (people_id, name))
    conn.commit()
    
    bot.send_message(people_id, "ID успешно изменён")

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    
    user_data = [message.chat.id, 0, name, password]
    cur.execute(f"INSERT INTO users VALUES(?,?,?,?)", user_data)
    bot.send_message(message.chat.id, f'Вы зарегистровались')
    
    conn.commit()
    cur.close()
    conn.close()
    
bot.polling(none_stop=True)