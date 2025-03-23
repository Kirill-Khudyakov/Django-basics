from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from csv import DictReader
from django.conf import settings



def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    current_page = int(request.GET.get('page', 1))

    with open(settings.BUS_STATION_CSV, encoding='utf-8') as file:
        reader = DictReader(file)
        stations = list(reader)

    paginator = Paginator(stations, 10)
    page = paginator.get_page(current_page)


    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
