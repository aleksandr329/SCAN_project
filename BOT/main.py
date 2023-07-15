import telebot
from constants import list_error, list_error2, string_error, TOKEN
from db import *
from logika import examination, lowercase_text
from zapros import get_zapros, category

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])  #<-- Функция приветствие
def start(message):
    text = f'''{message.from_user.first_name}, наш БОТ 🤖 может
    обрабатывать ваш запрос и предлогать вам тему новостей для просмотра!'''
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def text(message):     #<-- Функция обрабатывающая запросы пользователя
    text1 = lowercase_text(message.text)  #<--Обрабатываем запрос пользователя делая список из маленьких слов и убираем не нужные слова
    text2 = examination(text1)  #<-- Проверяем и выявляем тему по которой больше всего совпадений и получаем кортеж

    if text2 in list_error:  #<-- Логика если запрос пользователя не найден
        create_user(message.from_user.id, message.from_user.first_name)  #<--Записываем пользователя в таблицу
        create_pending_requests(message.from_user.id, text1)  #<-- Записываем не распознаный запрос
        bot.send_message(message.chat.id, text2, parse_mode='HTML')  #<--Выводим сообщение что запрос не распознан
        pass
    if text1[0] == list_error2[0] and text1[4] == list_error2[4]:  #<-- Условие которое отлавливает текст из сообщения
        pass

    elif text2[0] == string_error:  #<-- Условие которое отлавливает 2 сообщение если запрос не найден
        pass

    else:       #<-- Логика если запрос успешно обработан
        menu1 = telebot.types.InlineKeyboardMarkup()
        menu1.add(telebot.types.InlineKeyboardButton(text='ДА!', callback_data='yes'))
        menu1.add(telebot.types.InlineKeyboardButton(text='НЕТ', callback_data='no'))
        bot.send_message(message.chat.id, f'Возможно вы хотите просмотреть новости на тему: <b>{text2[0]} ?</b>', reply_markup=menu1, parse_mode='HTML')
        answer = similar_request(text1)
        bot.send_message(message.chat.id, f'Количество подобных запросов: <b>{answer[1]}</b>  \n\n<b>{answer[0]}</b> - пользователя сделали подобный запрос. ', parse_mode='HTML')
        create_processed_requests(message.from_user.id, message.from_user.first_name, text2[1], text1)  #<-- Функция записи запроса  если такой распознан

        return text1, text2


@bot.callback_query_handler(func=lambda call: True)
def button(call):
    if call.data == 'yes':  #<-- Логика если пользователь нажмет кнопку ДА
        zap = category(text(call.message)[1][1])
        novost = get_zapros(zap)
        for i in novost:
            bot.send_message(call.message.chat.id, i)

    if call.data == 'no':  #<-- Логика если пользователь нажмет кнопку НЕТ
        bot.send_message(call.message.chat.id, 'Введите пожалуйста ваш запрос заново.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
