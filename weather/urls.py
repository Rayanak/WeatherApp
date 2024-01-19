from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('weather/<int:id>/', views.weather_by_id, name='weather_by_id'),
    path('weather/<slug:city_name>/', views.weather_by_city, name='weather_by_city'),
]
