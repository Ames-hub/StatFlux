from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.creation_page, name='create'),
    path('delete/', views.delete_page, name='delete'),

    path('api/statistic_create', views.create_statistic, name='create_statistic'),
    path('api/statistic_delete', views.delete_statistic, name='delete_statistic'),
    path('api/list_statistics', views.list_statistics, name='list_statistics'),
    path('api/get_stat_data/<str:stat_name>', views.fetch_statistic_data, name='fetch_stat_data'),
    path('api/enter_stat_data', views.enter_stat_data, name='enter_stat_data'),

    path('view/<str:stat_name>/', views.view_statistic, name='view_statistic')
]
