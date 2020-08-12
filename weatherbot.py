import requests
from pprint import pprint

def get_weather_json(city : str) -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=e33716772526cb3ddd1e82ef41156a23&units=imperial')
    return get_request.json()

def get_dailyWeather_json(long : float, lat : float) -> dict:
    get_request = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat='+str(lat)+'&lon='+str(long)+'&exclude=[minutely,hourly]&appid=e33716772526cb3ddd1e82ef41156a23&units=imperial')
    return get_request.json()

def main():
    city = input('Enter a city: ')

    try:
        json_data = get_weather_json(city)
        coord = tuple(json_data['coord'].values())
        json_data = get_dailyWeather_json(*coord)
        daily_temps = [json_data['daily'][index]['temp'] for index in range(len(json_data['daily']))]
        pprint(daily_temps)

    except ValueError:
        print('There was an error attempting to get json data from one of the two provided urls')
        exit()

main()