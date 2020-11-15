import requests
import config
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import City
from .forms import CityForm


# Create your views here.

def delete_city(request):
    City.objects.filter(name=request.GET.get('city', '')).delete()
    return redirect('/')


def index(request):
    api_key = config.openweathermap_api_key
    cities = City.objects.all()
    all_cities = []

    if request.method == 'POST':
        if request.POST.get('send') == 'Find out the weather' and \
                not any(request.POST.get('name').lower() == city.name.lower() for city in cities.all()):
            form = CityForm(request.POST)
            form.save()
        else:
            messages.error(request, "This city has already added!")

    form = CityForm()

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={api_key}'
        response = requests.get(url).json()

        try:
            city_info = {
                'city': city.name.title(),
                'temp': response['main']['temp'],
                'icon': response['weather'][0]['icon']
            }

            all_cities.append(city_info)
        except KeyError:
            pass

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)
