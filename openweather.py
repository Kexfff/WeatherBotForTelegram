import requests
import json
from deep_translator import GoogleTranslator, single_detection
from utils import keys



def TranslateCityName(name):
    langToken = keys['detectlangToken']
    lang = single_detection(name, api_key=langToken)
    if lang != 'en':
        translatedEn = GoogleTranslator(source='auto', target='en').translate(name)
        nativeLang = name
    else:
        nativeLang = name
        translatedEn = name
    return translatedEn, nativeLang


def GetWeatherInCity(id):
    weatherToken = keys['openweatherToken']
    link = "http://api.openweathermap.org/data/2.5/weather?id=" + str(id)+ "&appid=" + weatherToken + "&units=metric"
    response = requests.get(link)
    resp = json.loads(response.text)
    temperature = resp['main']['temp']
    temp = str(temperature)
    return temp


def GetCities(name):
    translatedEn, nativeLang = TranslateCityName(name)
    citiesIds = JsonToList("city.list.json")
    cities = [element for element in citiesIds if element['name'] == translatedEn]
    if cities == []:
        cities = [element for element in citiesIds if element['name'] == nativeLang]
        if cities == []:
            return False
    return cities

def GetCityById(id):
    citiesIds = JsonToList("city.list.json")
    city = next((element for element in citiesIds if element['id'] == int(id)), False)
    if city == False:
        return False
    return city['name']

def JsonToList(name):
    with open(name, 'r', encoding='utf-8') as citiesIdsJsonFile:
        citiesIdsJson = citiesIdsJsonFile.read()
        citiesIds = json.loads(citiesIdsJson)
        return citiesIds
    print("Couldn't read the file")
