from django.http import HttpRequest
from django.shortcuts import render
from .forms import StatisticForm

def home(request: HttpRequest):
    return render(request, 'statsapp/home.html')

def create(request):
    form = StatisticForm()
    return render(request, 'statsapp/create_statistic.html', {'form': form})