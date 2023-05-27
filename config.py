from telebot import types

TOKEN = ''

#Reply Button 
MainBut0 = types.KeyboardButton('Регистрация')
MeinBut1 = types.KeyboardButton('Авторизация')

#InLine Button
updateBut = types.InlineKeyboardButton('обновить ваш ID', callback_data='update')

