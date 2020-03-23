import telebot
import content
import random
import requests
from telebot import types
from bs4 import BeautifulSoup as BS
token = "1033448651:AAFjnIlJAsReuPmjTj0yaou2XcB_QqoZUhs"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def welcome(message):
    img = open('picture.jpg', 'rb')
    bot.send_photo(message.chat.id, img )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Хочу анекдот")
    item2 = types.KeyboardButton("Хочу добрый мем")
    item3 = types.KeyboardButton("Узнать погоду в НН")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,"Привет, {0.first_name}!\nЯ - бот, созданный, чтобы отправлять тебе разные приколюхи:)".format(message.from_user, bot.get_me()), reply_markup=markup)



@bot.message_handler(content_types=['text'])
def sendSomething(message):
    if message.chat.type == 'private':
        if message.text == 'Хочу анекдот':
            rand_index_anek = random.randint(0, len(content.anekdot))
            bot.send_message(message.chat.id, content.anekdot[rand_index_anek])
        elif message.text == 'Хочу добрый мем':
            rand_index_mem = random.randint(0, len(content.mem))
            image = open(content.mem[rand_index_mem], 'rb')
            bot.send_photo(message.chat.id, image)
        elif message.text == 'Узнать погоду в НН':
            r = requests.get('https://sinoptik.ua/погода-нижний-новгород')
            html = BS(r.content, 'html.parser')

            for el in html.select('#content'):
                t_min = el.select('.temperature .min')[0].text
                t_max = el.select('.temperature .max')[0].text
                text = el.select('.wDescription .description')[0].text
                bot.send_message(message.chat.id, t_min + '\n' + t_max + '\n' + text)
        else:
            bot.send_message(message.chat.id, 'Я не понял, что ты от меня хочешь')


bot.polling(none_stop=True)