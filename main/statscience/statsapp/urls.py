from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.creation_page, name='create'),

    path('api/statistic_create', views.create_statistic, name='create_statistic'),
    path('api/list_statistics', views.list_statistics, name='list_statistics'),
]