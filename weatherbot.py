import requests
import discord
from discord.ext import commands 
from pprint import pprint

################ Weather API ############################# 

def get_weather_json(city : str) -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=e33716772526cb3ddd1e82ef41156a23&units=imperial')
    return get_request.json()

def get_dailyWeather_json(long : float, lat : float) -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat='+str(lat)+'&lon='+str(long)+'&exclude=[minutely,hourly]&appid=e33716772526cb3ddd1e82ef41156a23&units=imperial')
    return get_request.json()

###########################################################

################# Discord bot #############################

client = discord.Client()

@client.event
async def on_ready():
    print(f'We are logged in as {client.user}')

def get_overall_weather(message, city):
    try:
        json_data = get_weather_json(city)
        coord = tuple(json_data['coord'].values())
        json_data = get_dailyWeather_json(*coord)
    
    except ValueError or KeyError:
        message.channel.send('Please check for typos and try entering a city again.')
        client.close()
    
    else:
        return json_data

def get_current_weather(message, city):
    if message.content.startswith('!current'):
        json_data = get_overall_weather(message, city)
        return [json_data['current']['temp']]
    return None

def get_daily_weather(message, city):
    if message.content.startswith('!daily'):
        json_data = get_overall_weather(message, city)
        return [json_data['daily'][index]['temp'] for index in range(len(json_data['daily']))]
    return None

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    all_messages = message.content.split(' ')

    if message.content.find('!help') != -1:
        with open('helpcommands.txt') as tips:
            read_tips = tips.read()
            await message.channel.send(read_tips)

    elif len(all_messages) <= 1: 
        await message.channel.send('Please use the command !help to see other available commands.')

    city = ' '.join(all_messages[1:])
    current_weather = get_current_weather(message, city)
    daily_weather = get_daily_weather(message, city)

    if current_weather != None:
        await message.channel.send(current_weather)
    elif daily_weather != None:
        await message.channel.send(daily_weather)

client.run('NzQzMjExMjM5MTc3NzE1NzE3.XzRXZw.EgBiu1vNKle73P-5gQLJHn5S224') # Discord WeatherBot token