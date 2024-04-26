from django.shortcuts import render
import requests
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import CityForm
from .models import City
import g4f


def index(request):
    api_key = "21eaa93aac94cf80e43e54a634a56ea0"
    url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid="
        + api_key
    )

    # city = "Воронеж"
    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            "city": city.name,
            "temp": int(res["main"]["temp"]),
            "icon": res["weather"][0]["icon"],
        }
        if city_info not in all_cities:
            all_cities.append(city_info)

    message = f"сгенерируй текстовый мем в зависимости от погоды в данный момент в городе {city}"

    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo, messages=[{"role": "user", "content": message}]
    )

    context = {"all_info": all_cities, "form": form, "message": response}

    return render(request, "mem_weather/index.html", context)







# def mem_gpt(message: str) -> str:
#     response = g4f.ChatCompletion.create(model=g4f.models.gpt_35_turbo,
#                                          messages=[{"role": "user", "content": message}])
#     return response
#
# print(mem_gpt("сгенерируй текстовый мем в зависимости от погоды в данный момент в городе Воронеж"))
