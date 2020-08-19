import requests, discord, pytz
from discord.ext import commands 
from datetime import date
from re import split

################ Weather API ############################# 

def get_currentWeather_json(city : str, units : str='imperial') -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=&units='+units)
    return get_request.json()

def get_dailyWeather_json(long : float, lat : float, units : str='imperial') -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat='+str(lat)+'&lon='+str(long)+'&exclude=[minutely,hourly]&appid=&units='+units)
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
async def on_ready() -> None:
    print(f'We are logged in as {client.user}')

# credit goes to steve-gregory on StackOverflow for the concise method
def get_windDirection(wind_degrees : float) -> str:
    index = int((wind_degrees / 22.5)+.5)
    directions = ['N','NNE','NE','ENE',"E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return directions[(index % 16)]

def get_overall_weather(city : str, units : str) -> tuple:
    error_msg = 'Please check for typos and try entering a city again.'
    try:
        current_json = get_currentWeather_json(city, units)
        coord = tuple(current_json['coord'].values())
        daily_json = get_dailyWeather_json(*coord, units)
    
    except (ValueError, KeyError):
        return tuple(error_msg for _ in range(3))
    else:
        return coord, current_json, daily_json

def get_current_weather(city : str, units : str) -> tuple:
    coord, json_data, _ = get_overall_weather(city, units)
    return coord, json_data

def print_current_weather(current_weather : dict, weather_types : dict, format_dt : list) -> str:

    current_day = date(*format_dt).strftime('%A %d')
    max_temp = str(int(current_weather['main']['temp_max']))
    min_temp = str(int(current_weather['main']['temp_min']))
    weather_desc = current_weather['weather'][0]['description'].title()
    humidity = str(current_weather['main']['humidity'])
    wind = current_weather['wind']
    wind_direction = get_windDirection(wind['deg'])

    temps = '\t'+max_temp+'\u00B0'+'/'+ min_temp+'\u00B0'+'\t'
    weather_type = weather_desc + ' ' + weather_types[weather_desc] + '\t'
    repr_humidity =  'humidity: ' + humidity+"%"+ '\t'
    repr_wind = '💨' +  ' ' + wind_direction+ ' ' + str(wind['speed'])+' mph'

    return ('```' + current_day + temps + weather_type + repr_humidity + repr_wind + '```')

def get_daily_weather(city : str, units : str) -> tuple:
    coord, _, json_data = get_overall_weather(city, units)
    return coord, json_data

def print_daily_weather(daily_weather : dict, weather_types : dict, format_dt : list) -> str:
    weekly = []
    for index in range(len(daily_weather['daily'])):
        weekly.append(
           [
                date(format_dt[0], format_dt[1], format_dt[2]+index).strftime('%A %d'),
                str(int(daily_weather['daily'][index]['temp']['max'])),
                str(int(daily_weather['daily'][index]['temp']['min'])),
                daily_weather['daily'][index]['weather'][0]['description'],
                str(daily_weather['daily'][index]['humidity']),
                get_windDirection(daily_weather['daily'][index]['wind_deg']),
                daily_weather['daily'][index]['wind_speed']  
           ] 
        ) 

    weekly_list = []
    max_len = len('Wednesday')
    for index in range(len(weekly)):
        temps = weekly[index][1]+'\u00B0'+'/'+ weekly[index][2]+'\u00B0'
        weather_type = weekly[index][3].title() + ' ' + weather_types[weekly[index][3].title()]
        repr_humidity =  'humidity: ' + weekly[index][4]+"%"
        current_day = weekly[index][0].split(' ')
        day_num = max_len - len(current_day[0]) + 3
        update_format = '{0:>%d}{1:>%d}{2:>%d}{3:>%d}{4:>%d}{5:>4}{6:>4}{7:>10}' % (len(current_day[0]),day_num,13,29,15)
        weekly_list.append(update_format.format(*current_day,temps,weather_type,repr_humidity,'💨',weekly[index][5],str(weekly[index][-1])+' mph\n'))

    weekly_str = ''.join(weekly_list)
    weekly_str = '```' + weekly_str + '```'
    return weekly_str

async def help_command(message : str) -> None:
    if message.content.find('!help') != -1:
        with open('helpcommands.txt') as tips:
            read_tips = tips.read()
            await message.channel.send(read_tips)

@client.event
async def on_message(message : str) -> None:
    if message.author == client.user:
        return

    all_messages = message.content.split(' ')

    await help_command(message)

    if not message.content.startswith('!help') and \
    not message.content.startswith('!current') and \
    not message.content.startswith('!weekly'): 
        await message.channel.send('Please use the command !help to see available commands.')
        return

    city = ' '.join(all_messages[2:])
    daily_weather = ''

    units = 'imperial' # Farhenheit
    if all_messages[1] == '-C':
        units = 'metric' # Celsius
    elif all_messages[1] == '-F':
        units = 'imperial'
    else:
        city = ' '.join(all_messages[1:])

    coord, current_weather = get_current_weather(city, units)
    if message.content.startswith('!weekly'):
        coord, daily_weather = get_daily_weather(city, units)

    error_msg = 'Please check for typos and try entering a city again.'

    if current_weather == error_msg or daily_weather == error_msg or coord == error_msg:  
        await message.channel.send(error_msg)
        return

    formatted_str = get_formatted_timestamp(*coord)['formatted']
    formatted_date = split('[- ]', formatted_str)[0:3]
    formatted_date = list(map(lambda x : int(x), formatted_date))

    weather_types = {
                     'Broken Clouds' : '⛅',
                     'Scattered Clouds' : '☁️', 
                     'Few Clouds' : '⛅',
                     'Overcast Clouds' : '☁️',
                     'Clear Sky': '☀️',
                     'Light Rain': '🌦️',
                     'Light Intensity Shower Rain': '🌦️',
                     'Moderate Rain' : '🌧️',
                     'Thunderstorm With Rain' : '⛈️',
                     'Heavy Intensity Rain' : '🌧️',
                     'Shower Rain' : '🌧️'
                    }
    if message.content.startswith('!current'):
        await message.channel.send(print_current_weather(current_weather,weather_types,formatted_date))
    elif message.content.startswith('!weekly'):
        await message.channel.send(print_daily_weather(daily_weather,weather_types,formatted_date))

client.run('') # Discord WeatherBot token