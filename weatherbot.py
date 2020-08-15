import requests, discord, pytz
from discord.ext import commands 
from datetime import date
from re import split

################ Weather API ############################# 

def get_currentWeather_json(city : str) -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=&units=imperial')
    return get_request.json()

def get_dailyWeather_json(long : float, lat : float) -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat='+str(lat)+'&lon='+str(long)+'&exclude=[minutely,hourly]&appid=&units=imperial')
    return get_request.json()

###########################################################

################# Timezone API ############################

def get_formatted_timestamp(long : float, lat : float) -> dict:
    get_request = requests.get('http://api.timezonedb.com/v2.1/get-time-zone?key=&format=json&by=position&lat='+str(lat)+'&lng='+str(long))
    return get_request.json()

###########################################################

################# Discord bot #############################

client = discord.Client()

@client.event
async def on_ready():
    print(f'We are logged in as {client.user}')

# credit goes to steve-gregory on StackOverflow for the concise method
def get_windDirection(wind_degrees : float) -> str:
    index = int((wind_degrees / 22.5)+.5)
    directions = ['N','NNE','NE','ENE',"E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return directions[(index % 16)]

def get_overall_weather(city) -> tuple:
    error_msg = 'Please check for typos and try entering a city again.'
    try:
        current_json = get_currentWeather_json(city)
        coord = tuple(current_json['coord'].values())
        daily_json = get_dailyWeather_json(*coord)
    
    except ValueError:
        return tuple(error_msg for _ in range(3))
    except KeyError:
        return tuple(error_msg for _ in range(3))
    else:
        return coord, current_json, daily_json

def get_current_weather(city) -> tuple:
    coord, json_data, _ = get_overall_weather(city)
    return coord, json_data

def print_current_weather(current_weather, weather_types, format_dt) -> str:

    # current_day = date.today().strftime('%A %d')
    current_day = date(*format_dt).strftime('%A %d')
    max_temp = str(int(current_weather['main']['temp_max']))
    min_temp = str(int(current_weather['main']['temp_min']))
    weather_desc = current_weather['weather'][0]['description'].title()
    humidity = str(current_weather['main']['humidity'])
    wind = current_weather['wind']
    wind_direction = get_windDirection(wind['deg'])

    print(weather_desc)

    temps = '\t'+'**'+max_temp+'\u00B0'+'**'+'/'+ min_temp+'\u00B0'+'\t'
    weather_type = weather_desc + ' ' + weather_types[weather_desc] + '\t'
    repr_humidity =  'humidity: ' + humidity+"%"+ '\t'
    repr_wind = ':dash:' +  ' ' + wind_direction+ ' ' + str(wind['speed'])+' mph'

    return (current_day + temps + weather_type + repr_humidity + repr_wind)

def get_daily_weather(city) -> tuple:
    coord, _, json_data = get_overall_weather(city)
    return coord, json_data['daily']

def print_daily_weather():
    pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    all_messages = message.content.split(' ')

    if message.content.find('!help') != -1:
        with open('helpcommands.txt') as tips:
            read_tips = tips.read()
            await message.channel.send(read_tips)

    elif len(all_messages) <= 1 or \
    (not message.content.startswith('!current') and \
    not message.content.startswith('!daily')): 
        await message.channel.send('Please use the command !help to see available commands.')

    city = ' '.join(all_messages[1:])
    coord = current_weather = daily_weather = ''

    if message.content.startswith('!current'):
        coord, current_weather = get_current_weather(city)
    else:
        coord, daily_weather = get_daily_weather(city)

    error_msg = 'Please check for typos and try entering a city again.'

    if current_weather == error_msg or daily_weather == error_msg or coord == error_msg:  
        await message.channel.send(error_msg)
        return

    formatted_str = get_formatted_timestamp(*coord)['formatted']
    formatted_date = split('[- ]', formatted_str)[0:3]
    formatted_date = map(lambda x : int(x), formatted_date)

    weather_types = {'Broken Clouds' : ':white_sun_cloud:', 
                     'Few Clouds' : ':white_sun_small_cloud:',
                     'Overcast Clouds' : ':cloud:',
                     'Clear Sky': ':sunny:'
                    }

    if message.content.startswith('!current'):
        await message.channel.send(print_current_weather(current_weather,weather_types,formatted_date))
    else:
        await message.channel.send(daily_weather)

client.run('') # Discord WeatherBot token