import telebot
import config
import sqlite3

from sqlite3.dbapi2 import connect
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
name = None
people_id = None

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
    bot.send_message(message.chat.id, f'Привет👋🏻 \nЯ бот, работающий с базой данных SQLite3 \nЯ Ещё дорабатываюсь, поэтому часть функционала может не работать😢', parse_mode = 'html', reply_markup= murkup)
    
@bot.message_handler(content_types=['text'])
def reserch(message):
    if message.text == 'Регистрация':
        
        conn = sqlite3.connect('test.db')
        cur = conn.cursor()
    
        global people_id
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
            cur.execute(f"SELECT admin FROM users WHERE id = {people_id}")
            data1 = cur.fetchall()
            markup = types.InlineKeyboardMarkup()
            markup.add(config.adminBut)
            
            dat = ''
            for el in data1:
                dat += f"{el[0]}"
            
            cur.execute(f"SELECT name FROM users WHERE id = {people_id}")
            name = cur.fetchall()
            
            
            name1 =''
            for el in name:
                name1 += f"{el[0]}"
            
            if dat == '1':
                bot.send_message(message.chat.id, f"Вы успешно вошли✅, {name1}", reply_markup = markup)
            elif dat == '0':
                bot.send_message(message.chat.id,f"Добро пожаловать✅, {name1}" )
                userPanel(message)
            elif dat == '3':
                bot.send_message(message.chat.id,f"неизвестная ошибка авторизации {dat}" )
    
        cur.close()
        conn.close()
    if message.text.lower() == 'войти как юзер':
        userPanel(message)
        
@bot.callback_query_handler(func= lambda call: call.data =='adminPanel')
def adminPanel(call):
    global people_id
    markup  = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(config.repUserBut)
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    dat = ''
    
    for el in data:
        dat += f'имя: {el[2]} пароль: {el[3]} доступ: {el[1]}\n'
    
    bot.send_message(people_id, dat)
    bot.send_message(people_id, "Вы можете выбрать введя его имя или id\n Также вы можете войти как пользователь",
                     reply_markup= markup)
    
def userPanel(message):
    markup1 = types.InlineKeyboardMarkup()
    markup1.row(config.userBut0, config.userBut1)
    markup1.row(config.userBut2, config.userBut3)
    bot.send_message(message.chat.id, 'Выберете раздел который, хотите почитать', reply_markup = markup1)
    
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
    data = cur.fetchall()
    cur.execute(f"SELECT pass FROM users WHERE pass = '%s'" % (password) )
    data1 = cur.fetchone()
    
    dat = ''
    for el in data:
        dat+=f'{el[0]}'
    
    if data != None and data1 != None:
        global people_id
        people_id = message.chat.id 
        markup = types.InlineKeyboardMarkup()
        
        markup.add(config.updateBut)
    
        bot.send_message(people_id, f"Вы успешно авторизовались!🥳, {dat}", reply_markup=markup)
    else:
        bot.send_message(people_id, f"Что-то пошло не так возможно неверный логин или пароль.\nЕсли вы забыли пароль обратитесь к администратору😢😢😢")

@bot.callback_query_handler(func= lambda call: call.data =='update')
def updata(call):
    global people_id
    
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    
    cur.execute("UPDATE users SET id = ? WHERE name = ?", (people_id, name))
    conn.commit()
    
    bot.send_message(people_id, "ID успешно изменён✅")

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    
    user_data = [message.chat.id, 0, name, password]
    cur.execute(f"INSERT INTO users VALUES(?,?,?,?)", user_data)
    bot.send_message(message.chat.id, f'Вы зарегистрировались✅')
    
    conn.commit()
    cur.close()
    conn.close()
    
bot.polling(none_stop=True)