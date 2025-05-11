from .forms import NewStatisticForm, DeleteStatisticForm, EnterStatDataForm
from .library.database import database
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest

def home(request: HttpRequest):
    return render(request, 'statsapp/home.html')

def creation_page(request):
    form = NewStatisticForm()
    return render(request, 'statsapp/create_statistic.html', {'form': form})

def delete_page(request):
    form = DeleteStatisticForm()
    return render(request, 'statsapp/delete_statistic.html', {'form': form})

def create_statistic(request):
    if request.method == 'POST':
        form = NewStatisticForm(request.POST)
        if form.is_valid():
            database.create_new_statistic(
                statistic_name=form.cleaned_data['stat_name'],
                statistic_description=form.cleaned_data['stat_description'],
                statistic_type=form.cleaned_data['stat_type'],
            )
            return JsonResponse({'success': True, 'message': 'Statistic created successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def enter_stat_data(request):
    if request.method == 'POST':
        form = EnterStatDataForm(request.POST)
        if form.is_valid():
            database.enter_statistic_data(
                stat_name=request.POST['stat_name'],
                date=form.cleaned_data['stat_date'],
                value=form.cleaned_data['stat_value'],
            )
            return JsonResponse({'success': True, 'message': 'Data entered successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Only POST allowed'}, status=405)

def list_statistics(request):
    data = {}
    for stat in database.list_all_statistics():
        data[stat[0]] = {
            'description': stat[1],
            'type': stat[2],
            'trend_analysis': {
                'enabled': False,
                'condition': None,
            }
        }

    return JsonResponse(data, status=200)

def view_statistic(request, stat_name):
    form = EnterStatDataForm()

    condition = "W.I.P"
    cdn_start_date = 'W.I.P'

    return render(
        request,
        'statsapp/statisticview.html',
        {
            'stat_name': stat_name,
            'current_condition': condition,  # TODO: Replace with real data
            'condition_start_date': cdn_start_date,
            'form': form,
            }
        )

def fetch_statistic_data(request, stat_name):
    statistic = database.fetch_statistic_details(stat_name)
    data = database.fetch_statistic_data(stat_name)

    data = {
        'name': data['name'],
        'type': statistic['type'],
        'data': data['data'],
    }
    return JsonResponse(data, status=200)

def delete_statistic(request):
    if request.method == 'POST':
        form = DeleteStatisticForm(request.POST)
        if form.is_valid():
            database.delete_statistic(
                statistic_name=form.cleaned_data['stat_name'],
            )
            return JsonResponse({'success': True, 'message': 'Statistic deleted from memory.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)