import requests
import json
from deep_translator import GoogleTranslator, single_detection



def TranslateCityName(name):
    keysfile = open('apikeys.txt', 'r')
    keys = json.loads(keysfile.read())[0]
    langToken = keys['detectlangToken']
    lang = single_detection(name, api_key=langToken)
    if lang == 'ru':
        translatedEn = GoogleTranslator(source='auto', target='en').translate(name)
        translatedRu = name
    else:
        translatedRu = GoogleTranslator(source='auto', target='ru').translate(name)
        translatedEn = name
    return translatedEn, translatedRu


def GetWeatherInCity(id):
    keysfile = open('apikeys.txt', 'r')
    keys = json.loads(keysfile.read())[0]
    weatherToken = keys['openweatherToken']
    link = "http://api.openweathermap.org/data/2.5/weather?id=" + str(id)+ "&appid=" + weatherToken + "&units=metric"
    response = requests.get(link)
    resp = json.loads(response.text)
    temperature = resp['main']['temp']
    temp = str(temperature)
    return temp


def GetCities(name):
    with open ("city.list.json", 'r', encoding='utf-8') as citiesIdsJsonFile:
        citiesIdsJson = citiesIdsJsonFile.read()
    translatedEn, translatedRu = TranslateCityName(name)
    citiesIds = json.loads(citiesIdsJson)
    cities = [element for element in citiesIds if element['name'] == translatedEn]
    if cities == []:
        cities = [element for element in citiesIds if element['name'] == translatedRu]
        if cities == []:
            return False
    return cities

def GetCityById(id):
    with open ("city.list.json", 'r', encoding='utf-8') as citiesIdsJsonFile:
        citiesIdsJson = citiesIdsJsonFile.read()
    citiesIds = json.loads(citiesIdsJson)
    city = next((element for element in citiesIds if element['id'] == int(id)), False)
    if city == False:
        return False
    return city['name']
