from telegram.ext import CommandHandler
from telegram.ext import Updater
from openweather import GetCities, GetWeatherInCity, GetCityById
from utils import keys




telegramToken = keys['telegramToken']
updater = Updater(token=telegramToken)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me your city name, please")
    print(update.effective_chat.id)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def SetCity(update, context):
    city = ''
    if len(context.args) > 1:
        for item in context.args:
            if city == '':
                city = item
            else:
                city = city + ' ' + item
    else:
        city = context.args[0]
    cities = GetCities(city)
    if cities == False:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't find your city")
        return
    elif len(cities)>1:
        multicities=''
        i=1
        for item in cities:
            c = 'City: ' + item['name']
            country = ', Country: ' + item['country']
            id = ', Id: ' + str(item['id'])
            multicities = multicities + c + country + id + '\n'
        message = 'There are several cities with the same name. Please, choose yours and set the city with its id by typing /setid <your id here>  (without <>) \n\n'
        message = message + multicities
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return
    cityid = cities[0]['id']
    temp = GetWeatherInCity(cityid)
    message = 'Your city is set!! Current temperature is ' + temp
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def SetCityById(update, context):
    id = context.args[0]
    city = GetCityById(id)
    temp = GetWeatherInCity(id)
    message = 'Your city is ' + city + "! Current temperature is " + temp
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)



city_handler = CommandHandler('setcity', SetCity)
dispatcher.add_handler(city_handler)

cityid_handler = CommandHandler('setid', SetCityById)
dispatcher.add_handler(cityid_handler)





updater.start_polling()