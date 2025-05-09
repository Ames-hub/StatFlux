from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest
from .forms import StatisticForm
from .library.database import db

def home(request: HttpRequest):
    return render(request, 'statsapp/home.html')

def creation_page(request):
    form = StatisticForm()
    return render(request, 'statsapp/create_statistic.html', {'form': form})

def create_statistic(request):
    if request.method == 'POST':
        form = StatisticForm(request.POST)
        if form.is_valid():
            db.create_new_statistic(
                statistic_name=form.cleaned_data['stat_name'],
                statistic_description=form.cleaned_data['stat_description'],
                statistic_type=form.cleaned_data['stat_type'],
            )
            return JsonResponse({'success': True, 'message': 'Statistic created successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def list_statistics(request):
    pass