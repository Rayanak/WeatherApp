import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def getCityLatLong(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
    r = requests.get(url.format(city_name)).json()

    if 'coord' in r:
        return {'lat': r['coord']['lat'], 'lon': r['coord']['lon']}
    else:
        # Возвращаем значение по умолчанию или обрабатываем ошибку
        return {'lat': 0, 'lon': 0}  # или возврат ошибки


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
    city = 'London'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        ya_city_weather = get_yandex_weather(city.name)
        city_weather = {
            'id': city.id,
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'desc_ya': ya_city_weather.get('description', '-'),
            'temp_ya': ya_city_weather.get('temperature', '0')
        }


        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def get_yandex_weather(city_name):
    url = "https://api.weather.yandex.ru/v2/forecast?"
    headers = {"X-Yandex-API-Key": "40fbfa7f-cf08-41c2-a18b-734c404c5215"}
    coord = getCityLatLong(city_name)
    print(coord)
    params = {"lat": coord['lat'], "lon": coord['lon'], "lang": "ru_RU"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        weather_data = response.json()
        forecast = weather_data.get("forecasts", [])[0]  # Получаем прогноз на ближайший день
        parts = forecast.get("parts", {})
        day_forecast = parts.get("day", {})  # Получаем дневной прогноз

        city_weather = {
            'city': city_name,
            'temperature': day_forecast.get("temp_avg"),  # Средняя температура
            'description': day_forecast.get("condition"),  # Погодное условие
            'wind_speed': day_forecast.get("wind_speed"),  # Скорость ветра
        }
    except requests.RequestException as e:
        city_weather = {'error': 'Не удалось получить данные о погоде'}

    return city_weather


def weather_by_id(request, id):
    city = City.objects.get(id=id)
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
    r = requests.get(url.format(city.name)).json()

    city_weather = {
        'city': city.name,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    context = {'city_weather': city_weather}
    return render(request, 'weather/weather_by_id.html', context)


def weather_by_city(request, city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c56398aa9dd4ea5e0854302e39acf5a5'
    r = requests.get(url.format(city_name)).json()

    city_weather = {
        'city': city_name,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    context = {'city_weather': city_weather}
    return render(request, 'weather/weather_by_city.html', context)
