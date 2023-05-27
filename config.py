from telebot import types

TOKEN = '6126298337:AAGwS0gCeDYA32MKtupNRacdJ8wAYfxW4jw'

#Reply Button 
MainBut0 = types.KeyboardButton('Регистрация')
MeinBut1 = types.KeyboardButton('Авторизация')

#InLine Button
updateBut = types.InlineKeyboardButton('обновить ваш ID', callback_data='update')

